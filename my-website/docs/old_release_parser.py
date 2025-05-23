import argparse
import os
import requests
import json
from urllib.parse import urlparse

def get_raw_readme(repo_link):
    if "raw.githubusercontent.com" in repo_link and repo_link.endswith(".md"):
        resp = requests.get(repo_link)
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(f"Could not fetch raw README.md, status code {resp.status_code}")
    
    if "github.com" in repo_link and "/blob/" in repo_link:
        parts = repo_link.split('/')
        user = parts[3]
        repo = parts[4]
        blob_idx = parts.index("blob")
        branch = parts[blob_idx+1]
        path = '/'.join(parts[blob_idx+2:])
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        resp = requests.get(raw_url)
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(f"Could not fetch README.md from the blob link. Tried: {raw_url}")

    # Standard repo URL
    if repo_link.endswith("/"):
        repo_link = repo_link[:-1]
    parsed = urlparse(repo_link)
    path = parsed.path.strip("/")
    for branch in ['main', 'master']:
        raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
        resp = requests.get(raw_url)
        if resp.status_code == 200:
            return resp.text
    raise Exception("Could not fetch README.md from the provided repo link.")

def save_file(folder, fname, content, tags, github_link=None):
    tag_yaml = "---\ntags:\n"
    for tag in tags:
        tag_yaml += f"  - {tag}\n"
    tag_yaml += "---\n\n"
    md = tag_yaml
    if github_link:
        md += f'[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)]({github_link})\n\n'
    md += content.strip() + "\n"
    with open(os.path.join(folder, fname), "w", encoding="utf-8") as f:
        f.write(md)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_link', type=str, required=True)
    parser.add_argument('--project_name', type=str, required=True)
    parser.add_argument('--output_folder', type=str, default='.')
    parser.add_argument('--tags', nargs='+', default=[])
    args = parser.parse_args()

    # Build the output directory
    folder = os.path.join(args.output_folder, args.project_name)
    os.makedirs(folder, exist_ok=True)

    readme = get_raw_readme(args.repo_link)

    repo_home = args.repo_link
    if "/blob/" in repo_home:
        repo_home = repo_home.split("/blob/")[0]

    # Save the entire README as <project_name>.md
    save_file(folder, f"{args.project_name}.md", readme, args.tags, github_link=repo_home)

    # Always create the following markdown files with stub content
    stubs = {
        "how-to.md": "## How-To Guides\n\nComing soon!",
        "explanation.md": "## Explanation\n\nComing soon!",
        "tutorial.md": "## Tutorial\n\nComing soon!",
    }
    for fname, content in stubs.items():
        save_file(folder, fname, content, args.tags)

    # Create _category_.json
    cat_json = {
        "label": args.project_name,
        "link": {"type": "generated-index"}
    }
    with open(os.path.join(folder, "_category_.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(cat_json, indent=2) + "\n")

if __name__ == "__main__":
    main()
