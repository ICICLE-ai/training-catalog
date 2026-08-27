#!/usr/bin/env python3
"""release_notes.py — helpers for the ICICLE release-notes skill.

**Standard library only** — runs with any `python3`, no venv needed.

Subcommands:
  collect   Classify a release's components into "new" vs "changelog" and pull the
            fields the notes need (name, componentVersion, primaryThrust,
            description, sourceCodeUrl) out of release_catalog.yml.
  render    Fill ICICLE-Release-Template.md from a collect payload and write
            ICICLE-Release-<YYYY-MM>.md.

New-vs-changelog is decided from the *deployed doc's* accumulated `Release YYYY-MM`
frontmatter tags, not the catalog id — ids get renamed between releases, tags don't.
"""

import argparse
import json
import pathlib
import re
import sys

# primaryThrust -> (section, subheading). Order here is the order they are emitted.
THRUST_MAP = {
    "core/CI4AI":       ("Intelligent Cyberinfrastructure", "CI-for-AI"),
    "core/AI4CI":       ("Intelligent Cyberinfrastructure", "AI-for-CI"),
    "core/Software":    ("Intelligent Cyberinfrastructure", "Software Architecture and Design"),
    "core/FoundationAI": ("Intelligent Cyberinfrastructure", "AI Foundations"),
    "useInspired/SF":   ("Use Inspired Science", "Smart Foodsheds"),
    "useInspired/AE":   ("Use Inspired Science", "Animal Ecology"),
    "useInspired/DA":   ("Use Inspired Science", "Digital Agriculture"),
}
# PADI and VA are retired: no component is released under them any more, and the
# template has no heading for either. A component still carrying one of these as its
# primaryThrust always carries at least one other canonical tag, and that tag decides
# its release-note category. Same for any thrust that isn't in THRUST_MAP.
RETIRED_THRUSTS = {"core/PADI", "core/VA"}

# Canonical README tag -> (section, subheading). Consulted only as the fallback,
# in template order: Intelligent Cyberinfrastructure first, then Use Inspired Science.
TAG_MAP = {
    "CI4AI":              ("Intelligent Cyberinfrastructure", "CI-for-AI"),
    "AI4CI":              ("Intelligent Cyberinfrastructure", "AI-for-CI"),
    "Software":           ("Intelligent Cyberinfrastructure", "Software Architecture and Design"),
    "Foundation-AI":      ("Intelligent Cyberinfrastructure", "AI Foundations"),
    "Smart-Foodsheds":    ("Use Inspired Science", "Smart Foodsheds"),
    "Animal-Ecology":     ("Use Inspired Science", "Animal Ecology"),
    "Digital-Agriculture": ("Use Inspired Science", "Digital Agriculture"),
}
TAG_PRIORITY = list(TAG_MAP)  # first match wins

SECTION_ORDER = ["Intelligent Cyberinfrastructure", "Use Inspired Science"]
SUB_ORDER = [v[1] for v in THRUST_MAP.values()]


# ---------------------------------------------------------------- catalog parsing
def parse_catalog(path):
    """Line-based read of release_catalog.yml.

    The file is uniformly `  - id: <x>` followed by `    key: value` lines, so a
    full YAML parser isn't needed (and would pull in a third-party dependency).
    Block scalars (`>` / `|`) are folded into one line.
    """
    entries = []
    cur = None
    pending_key = None
    pending = []
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        m_id = re.match(r"^\s*-\s+id:\s*(.+?)\s*$", raw)
        if m_id:
            if cur is not None:
                if pending_key:
                    cur[pending_key] = " ".join(pending).strip()
                entries.append(cur)
            cur = {"id": m_id.group(1).strip().strip('"\'')}
            pending_key, pending = None, []
            continue
        if cur is None:
            continue
        m_kv = re.match(r"^\s{2,}([A-Za-z][\w]*):\s*(.*)$", raw)
        if m_kv:
            if pending_key:
                cur[pending_key] = " ".join(pending).strip()
                pending_key, pending = None, []
            key, val = m_kv.group(1), m_kv.group(2).strip()
            # Block scalars (`>` / `|`) AND a bare `key:` with the value on the
            # following indented line (a plain multi-line scalar) both continue.
            # If nothing follows, the pending flush yields "" — same as an empty value.
            if val in (">", "|", ">-", "|-", ""):
                pending_key, pending = key, []
            else:
                cur[key] = val.strip('"\'')
        elif pending_key and raw.strip():
            pending.append(raw.strip())
    if cur is not None:
        if pending_key:
            cur[pending_key] = " ".join(pending).strip()
        entries.append(cur)
    return entries


def doc_frontmatter_tags(docs_dir, component):
    """All frontmatter tags on a component's main doc, in file order ([] if none)."""
    folder = pathlib.Path(docs_dir) / component
    if not folder.is_dir():
        return None
    mains = [p for p in folder.glob("*.md")
             if p.stem.lower() not in ("how-to", "explanation", "explanations",
                                       "tutorials", "tutorial")]
    if not mains:
        return None
    # prefer the file named after the folder
    main = next((p for p in mains if p.stem == component), mains[0])
    text = main.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    scope = fm.group(1) if fm else text
    return [m.strip() for m in re.findall(r"^\s*-\s+(.+?)\s*$", scope, re.M)]


def prior_releases(tags, release):
    """The `Release YYYY-MM` tags other than this release's."""
    found = [re.match(r"Release (\d{4}-\d{2})$", t) for t in tags]
    return sorted({m.group(1) for m in found if m and m.group(1) != release})


def resolve_heading(thrust, tags):
    """(section, subheading, why) for a component.

    primaryThrust decides it when that thrust is live. When the thrust is retired
    (PADI / VA) or unrecognised, fall back to the component's other canonical tags —
    such a component always carries one — taking the first in template order.
    """
    if thrust in THRUST_MAP and thrust not in RETIRED_THRUSTS:
        return (*THRUST_MAP[thrust], f"primaryThrust {thrust}")
    for tag in TAG_PRIORITY:
        if tag in tags:
            reason = ("retired thrust " + thrust) if thrust in RETIRED_THRUSTS \
                else (f"unmapped thrust {thrust!r}" if thrust else "no thrust")
            return (*TAG_MAP[tag], f"{reason} -> tag {tag}")
    return (None, None, f"no usable thrust or tag (thrust={thrust!r}, tags={tags})")


def slugify(folder):
    """Docusaurus category slug for a docs folder name (lowercase, spaces->-, & dropped)."""
    return re.sub(r"-+", "-", folder.lower().replace("&", "").replace(" ", "-")).strip("-")


def norm_version(v):
    v = str(v or "").strip().strip('"\'')
    return v if v.lower().startswith("v") else f"v{v}"


# ---------------------------------------------------------------------- collect
def cmd_collect(a):
    entries = parse_catalog(a.catalog)
    by_release = [e for e in entries
                  if str(e.get("targetIcicleRelease", "")).strip().strip('"\'') == a.release]
    if not by_release:
        sys.exit(f"no catalog entries with targetIcicleRelease: {a.release}")

    docs_root = pathlib.Path(a.docs)
    folders = {p.name: p for p in docs_root.iterdir() if p.is_dir()} if docs_root.is_dir() else {}

    out = {"release": a.release, "new": [], "changelog": [], "unmapped": [], "no_doc": []}
    rows = []
    for e in by_release:
        name = e.get("name", "").strip()
        thrust = e.get("primaryThrust", "").strip()
        # Match the doc folder. `trainingTutorialsUrl` is authoritative: icicle-release
        # builds it from the deployed folder's Docusaurus slug, so it survives the
        # catalog `name` differing from the folder name ("ArrayMorph for Cloud HDF5"
        # vs docs/ArrayMorph). Fall back to name matching only if it's absent.
        folder = None
        tut = (e.get("trainingTutorialsUrl") or "").rstrip("/")
        if "/docs/category/" in tut:
            want = tut.rsplit("/", 1)[-1].lower()
            for cand in folders:
                if slugify(cand) == want:
                    folder = cand
                    break
        if folder is None:
            for cand in folders:
                if cand.lower() == name.lower():
                    folder = cand
                    break
        if folder is None:
            for cand in folders:
                squashed = re.sub(r"[^a-z0-9]", "", cand.lower())
                if squashed and squashed == re.sub(r"[^a-z0-9]", "", name.lower()):
                    folder = cand
                    break
        tags = doc_frontmatter_tags(a.docs, folder) if folder else None
        tags = tags or []
        prior = prior_releases(tags, a.release)
        section, sub, why = resolve_heading(thrust, tags)

        item = {
            "id": e.get("id"), "name": name,
            "version": norm_version(e.get("componentVersion")),
            "thrust": thrust, "tags": tags,
            "section": section, "subheading": sub, "heading_reason": why,
            "description": " ".join((e.get("description") or "").split()),
            "url": e.get("sourceCodeUrl", "").strip(),
            "doc_folder": folder, "prior_releases": prior,
        }
        if section is None:
            out["unmapped"].append(item)
            bucket = "UNMAPPED"
        elif folder is None:
            out["no_doc"].append(item)
            bucket = "NO DOC"
        elif prior:
            out["changelog"].append(item)
            bucket = "changelog"
        else:
            out["new"].append(item)
            bucket = "new"
        rows.append((name, item["version"], bucket, sub or "-", why))

    w = max(len(r[0]) for r in rows) + 2
    print(f"{'COMPONENT'.ljust(w)}{'VERSION':10}{'BUCKET':11}{'SUBHEADING':34}WHY")
    for r in sorted(rows, key=lambda x: (x[2], x[0])):
        print(f"{r[0].ljust(w)}{r[1]:10}{r[2]:11}{r[3]:34}{r[4]}")
    print(f"\nnew={len(out['new'])}  changelog={len(out['changelog'])}"
          f"  unmapped={len(out['unmapped'])}  no_doc={len(out['no_doc'])}")
    fellback = [i for i in out["new"] + out["changelog"]
                if "-> tag " in i["heading_reason"]]
    if fellback:
        print("note: categorised from tags rather than primaryThrust —",
              ", ".join(f"{i['name']} ({i['heading_reason']})" for i in fellback))
    if out["unmapped"]:
        print("!! no usable thrust or canonical tag — needs a manual heading:",
              ", ".join(f"{i['name']} ({i['thrust']}, tags={i['tags']})"
                        for i in out["unmapped"]))
    if out["no_doc"]:
        print("!! in catalog but no deployed doc:",
              ", ".join(i["name"] for i in out["no_doc"]))

    # Release-note links must point at the ICICLE-ai org (or a non-GitHub host such as
    # Hugging Face). A GitHub URL under any other org means the component's upstream
    # sourceCodeUrl still names a lab/personal fork — surface it rather than publishing it.
    stray = [i for i in out["new"] + out["changelog"]
             if "github.com/" in i["url"] and "github.com/ICICLE-ai/" not in i["url"]]
    if stray:
        print("!! non-ICICLE-ai GitHub links (fix sourceCodeUrl upstream, then re-append):")
        for i in stray:
            print(f"     {i['name']}: {i['url']}")

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {a.out}")


# ----------------------------------------------------------------------- render
def render_block(items):
    """Group items by their resolved section/subheading and emit template markdown."""
    lines = []
    for section in SECTION_ORDER:
        subs = [s for s in SUB_ORDER
                if any(i["section"] == section and i["subheading"] == s for i in items)]
        # de-dup while preserving order (template lists one heading twice)
        seen = set()
        subs = [s for s in subs if not (s in seen or seen.add(s))]
        if not subs:
            continue
        lines.append(f"## {section}")
        for sub in subs:
            group = [i for i in items
                     if i["section"] == section and i["subheading"] == sub]
            lines.append(f"### {sub}")
            for i in sorted(group, key=lambda x: x["name"].lower()):
                lines.append(f'- [**{i["name"]} {i["version"]}**]({i["url"]})')
                lines.append(f'    - {i["description"]}')
            lines.append("")
    return "\n".join(lines).rstrip()


def cmd_render(a):
    data = json.loads(pathlib.Path(a.data).read_text(encoding="utf-8"))
    rel = data["release"]
    tpl = pathlib.Path(a.template).read_text(encoding="utf-8")

    # Everything from '# New to ICICLE CI Catalog' up to the Changelog heading is the
    # sample body; likewise the Changelog heading up to the closing boilerplate.
    m_new = re.search(r"^# New to ICICLE CI Catalog\s*$", tpl, re.M)
    m_chg = re.search(r"^# NSF ICICLE CI Components Changelog\s*$", tpl, re.M)
    if not (m_new and m_chg):
        sys.exit("template is missing the 'New to ICICLE CI Catalog' or "
                 "'NSF ICICLE CI Components Changelog' heading")
    # the footer starts at the first paragraph after the Changelog heading
    after = tpl[m_chg.end():]
    m_foot = re.search(r"^The ICICLE team is committed", after, re.M)
    footer = after[m_foot.start():] if m_foot else after.lstrip("\n")

    head = tpl[:m_new.start()]
    new_md = render_block(data["new"]) or "_No new components in this release._"
    chg_md = render_block(data["changelog"]) or "_No component updates in this release._"

    doc = (f"{head}"
           f"# New to ICICLE CI Catalog\n\n{new_md}\n\n\n"
           f"# NSF ICICLE CI Components Changelog\n\n{chg_md}\n\n\n"
           f"{footer}")
    doc = doc.replace("YYYY-MM", rel)

    pathlib.Path(a.out).write_text(doc, encoding="utf-8")
    left = doc.count("YYYY-MM")
    print(f"wrote {a.out}  (new={len(data['new'])}, changelog={len(data['changelog'])}, "
          f"unresolved YYYY-MM placeholders={left})")
    if left:
        sys.exit("!! placeholders remain — inspect the output")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("collect", help="classify components and pull catalog fields")
    c.add_argument("--release", required=True, help="YYYY-MM")
    c.add_argument("--catalog", required=True, help="path to release_catalog.yml")
    c.add_argument("--docs", required=True, help="path to my-website/docs")
    c.add_argument("--out", required=True, help="JSON payload to write")
    c.set_defaults(func=cmd_collect)

    r = sub.add_parser("render", help="fill the template from a collect payload")
    r.add_argument("--data", required=True)
    r.add_argument("--template", required=True)
    r.add_argument("--out", required=True)
    r.set_defaults(func=cmd_render)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
