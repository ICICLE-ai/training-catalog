import argparse
import os
import re
import json
import requests
import pandas as pd  # required only if --excel_file is used
from urllib.parse import urlparse
from typing import List, Optional, Tuple, Dict

# -----------------------------
# GitHub helpers
# -----------------------------

def build_requests_session(github_pat: Optional[str] = None) -> requests.Session:
    """
    Create a requests session. If a GitHub PAT is provided (explicit arg or env),
    attach it as an Authorization header so private repos can be accessed.
    """
    token = github_pat or os.getenv("GITHUB_PAT")
    sess = requests.Session()
    if token:
        sess.headers.update({"Authorization": f"token {token.strip()}"})
    # Basic accept header is sometimes helpful for GitHub endpoints
    sess.headers.update({"Accept": "application/vnd.github.v3.raw"})
    return sess

def to_raw_readme_url(repo_link: str) -> Optional[str]:
    """
    Convert a normal GitHub URL to the corresponding raw.githubusercontent URL for README.md.
    Handles:
      - direct raw (returns as-is)
      - blob links (converts)
      - repo root links (tries main/master README.md)
    Returns None if conversion cannot be determined (rare).
    """
    if "raw.githubusercontent.com" in repo_link and repo_link.endswith(".md"):
        return repo_link  # already raw

    if "github.com" in repo_link and "/blob/" in repo_link:
        # e.g., https://github.com/user/repo/blob/branch/path/README.md
        parts = repo_link.split("/")
        # parts: ['https:', '', 'github.com', user, repo, 'blob', branch, path...]
        if len(parts) >= 7:
            user, repo, branch = parts[3], parts[4], parts[6]
            path = "/".join(parts[7:])  # includes README.md file
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        return None

    # Standard repo URL (root, with or without trailing slash)
    parsed = urlparse(repo_link.rstrip("/"))
    if parsed.netloc == "github.com":
        path = parsed.path.strip("/")  # user/repo or user/repo/...
        if path.count("/") >= 1:
            user_repo = "/".join(path.split("/")[:2])
            # We'll try 'main' then 'master'
            for branch in ["main", "master"]:
                raw_url = f"https://raw.githubusercontent.com/{user_repo}/{branch}/README.md"
                # Don't fetch here; just return the first candidate. The caller can try both.
                # But to be robust, we return a list or let the fetcher test both.
                # We'll let get_raw_readme() handle the branch attempts.
            return f"https://raw.githubusercontent.com/{user_repo}/main/README.md"  # default try main first
    return None

def fetch_raw_readme(repo_link: str, session: requests.Session) -> str:
    """
    Fetch README content as text using a raw URL. Supports:
      - raw links
      - /blob/ links converted to raw
      - repo root links: tries main then master
    Raises Exception on failure.
    """
    # Case 1: raw or blob → raw
    raw_candidate = to_raw_readme_url(repo_link)
    if raw_candidate and "raw.githubusercontent.com" in raw_candidate:
        resp = session.get(raw_candidate)
        if resp.status_code == 200:
            return resp.text
        # If it was a root link defaulting to main, try master as a fallback
        if "/main/" in raw_candidate:
            fallback = raw_candidate.replace("/main/", "/master/")
            resp2 = session.get(fallback)
            if resp2.status_code == 200:
                return resp2.text
        raise Exception(f"Could not fetch README.md, status code {resp.status_code} for {raw_candidate}")

    # Case 2: Standard repo URL we couldn't transform—try main/master explicitly
    parsed = urlparse(repo_link.rstrip("/"))
    path = parsed.path.strip("/")
    for branch in ["main", "master"]:
        raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
        resp = session.get(raw_url)
        if resp.status_code == 200:
            return resp.text

    raise Exception("Could not fetch README.md from the provided repo link.")

def repo_home_url(repo_link: str) -> str:
    """
    Return the 'home' URL of the repo (no /blob/...). Useful for the badge link.
    """
    if "/blob/" in repo_link:
        return repo_link.split("/blob/")[0]
    return repo_link.rstrip("/")

def derive_project_name(repo_link: str) -> str:
    """
    Derive a project name from a repo URL if none is given.
    Uses the repository name portion.
    """
    parsed = urlparse(repo_link.rstrip("/"))
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[1]
    # Fallback: last path segment
    return parts[-1] if parts else "project"

# -----------------------------
# Content splitting & mapping
# -----------------------------

SECTION_SPLIT_REGEX = r"^\s*---\s*$"  # line containing only '---'
SECTION_PATTERN = re.compile(SECTION_SPLIT_REGEX, flags=re.MULTILINE)

# Map target filenames to heading patterns (case-insensitive)
HEADING_MAP: Dict[str, List[re.Pattern]] = {
    "tutorials.md": [
        re.compile(r"^\s*#\s*tutorials?\s*$", re.IGNORECASE | re.MULTILINE)
    ],
    "how-to.md": [
        re.compile(r"^\s*#\s*how[-\s]*to\s*guides?\s*$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*#\s*how[-\s]*to\s*guide\s*$", re.IGNORECASE | re.MULTILINE),
    ],
    "explanation.md": [
        re.compile(r"^\s*#\s*explanations?\s*$", re.IGNORECASE | re.MULTILINE)
    ],
}

# -----------------------------
# File helpers
# -----------------------------

def tag_block(tags: List[str]) -> str:
    """Create a YAML frontmatter tag block."""
    unique = []
    seen = set()
    for t in tags:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    lines = ["---", "tags:"]
    for tag in unique:
        lines.append(f"  - {tag}")
    lines.append("---\n")
    return "\n".join(lines)

def save_file(folder: str, fname: str, content: str, tags: List[str], github_link: Optional[str] = None):
    """
    Save a Markdown file with frontmatter and optional GitHub badge.
    """
    os.makedirs(folder, exist_ok=True)
    md = tag_block(tags)
    if github_link:
        md += f'[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)]({github_link})\n\n'
    md += content.strip() + "\n"
    with open(os.path.join(folder, fname), "w", encoding="utf-8") as f:
        f.write(md)

def write_category_json(folder: str, project_name: str):
    """
    Write Docusaurus _category_.json to let the folder render a generated index.
    """
    cat_json = {
        "label": project_name,
        "link": {"type": "generated-index"}
    }
    with open(os.path.join(folder, "_category_.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(cat_json, indent=2) + "\n")

# -----------------------------
# Processing pipeline
# -----------------------------

def split_sections(readme_text: str) -> List[str]:
    """
    Split README text into sections using lines that contain only '---'.
    """
    parts = re.split(SECTION_PATTERN, readme_text)
    # Strip trailing whitespace from each part
    return [p.strip() for p in parts if p.strip()]

def classify_and_write_sections(
    folder: str,
    parts: List[str],
    base_tags: List[str],
    repo_link_for_badge: str,
    project_name: str,
    release: Optional[str] = None
):
    """
    - Save the first section as {project_name}.md (with optional Release tag injected only here)
    - For the remaining sections, detect headings and save into tutorials.md, how-to.md, explanation.md.
      If a section matches multiple categories (unlikely), first match wins.
    """
    # First part → main file; add Release tag if provided
    main_tags = list(base_tags)
    if release:
        main_tags.append(f"Release {release}")

    save_file(
        folder=folder,
        fname=f"{project_name}.md",
        content=parts[0],
        tags=main_tags,
        github_link=repo_link_for_badge
    )

    written = set()
    for part in parts[1:]:
        assigned = False
        for out_name, patterns in HEADING_MAP.items():
            if out_name in written:
                continue
            if any(p.search(part) for p in patterns):
                save_file(folder, out_name, part, base_tags)
                written.add(out_name)
                assigned = True
                break
        # If not assigned, you could choose to skip or dump to 'extras.md'
        # Here we skip silently.

def process_single_repo(
    repo_link: str,
    project_name: Optional[str],
    output_folder: str,
    tags: List[str],
    release: Optional[str],
    session: requests.Session
):
    """
    Process a single repo:
      - fetch README
      - split into sections
      - write markdown files and category json
    """
    repo_name = project_name or derive_project_name(repo_link)
    project_folder = os.path.join(output_folder, repo_name)
    os.makedirs(project_folder, exist_ok=True)

    readme_text = fetch_raw_readme(repo_link, session)
    parts = split_sections(readme_text)

    repo_home = repo_home_url(repo_link)

    if not parts:
        # No content; write an empty main file at least
        save_file(project_folder, f"{repo_name}.md", "", (tags + ([f"Release {release}"] if release else [])), github_link=repo_home)
    else:
        classify_and_write_sections(
            folder=project_folder,
            parts=parts,
            base_tags=tags,
            repo_link_for_badge=repo_home,
            project_name=repo_name,
            release=release
        )

    write_category_json(project_folder, repo_name)

# -----------------------------
# Excel helpers
# -----------------------------

def read_repos_from_excel(xlsx_path: str) -> List[Tuple[str, Optional[str]]]:
    """
    Reads an Excel file and returns a list of (repo_link, project_name_opt).
    Requires a column named 'README' containing normal GitHub links (not raw).
    Uses column 'Component' as the project name if available.
    """
    df = pd.read_excel(xlsx_path)
    if "README" not in df.columns:
        raise ValueError("Excel file must contain a column named 'README' with GitHub links.")
    
    repos: List[Tuple[str, Optional[str]]] = []
    has_component = "Component" in df.columns

    for _, row in df.iterrows():
        link = str(row["README"]).strip()
        if not link or link.lower() == "nan":
            continue
        proj = str(row["Component"]).strip() if has_component and not pd.isna(row["Component"]) else None
        repos.append((link, proj))
    return repos

# -----------------------------
# CLI
# -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch README from GitHub repos and split into docs sections.")
    # Single-run options
    parser.add_argument("--repo_link", type=str, help="GitHub repository URL or README blob URL (non-raw).")
    parser.add_argument("--project_name", type=str, help="Project name (folder and main file). If omitted, derived from repo URL.")
    # Batch mode via Excel
    parser.add_argument("--excel_file", type=str, help="Path to an Excel file containing a 'README' column with GitHub links and optional 'Project' column.")
    # Output and metadata
    parser.add_argument("--output_folder", type=str, default=".", help="Output root folder (defaults to current directory).")
    parser.add_argument("--tags", nargs="+", default=[], help="Base tags to include in all generated files.")
    parser.add_argument("--release", type=str, help="Release in 'YYYY-MM' format. Adds a 'Release YYYY-MM' tag to the main project file.")
    # Auth
    parser.add_argument("--github_pat", type=str, help="Optional GitHub PAT (overrides GITHUB_PAT env var).")
    return parser.parse_args()

def main():
    args = parse_args()
    session = build_requests_session(args.github_pat)

    # Validation: either single mode or excel mode must be present
    if not args.excel_file and not args.repo_link:
        raise SystemExit("Provide either --repo_link for single-run OR --excel_file for batch processing.")

    if args.excel_file:
        repos = read_repos_from_excel(args.excel_file)
        if not repos:
            raise SystemExit("No valid rows found in the Excel file.")
        for repo_link, proj_name in repos:
            process_single_repo(
                repo_link=repo_link,
                project_name=proj_name or args.project_name,  # allow CLI to override, else use Excel, else derive
                output_folder=args.output_folder,
                tags=args.tags,
                release=args.release,
                session=session
            )
    else:
        # Single repo path
        process_single_repo(
            repo_link=args.repo_link,
            project_name=args.project_name,
            output_folder=args.output_folder,
            tags=args.tags,
            release=args.release,
            session=session
        )

if __name__ == "__main__":
    main()
