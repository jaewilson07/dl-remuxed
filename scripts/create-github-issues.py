#!/usr/bin/env python3
"""
Create GitHub issues from markdown files using PyGithub.

Usage:
    # Set your GitHub token
    $env:GITHUB_TOKEN = "your-github-token"

    # Run the script
    python scripts/create-github-issues.py
"""

import os
import re
from pathlib import Path

from github import Github


def parse_issue_file(filepath):
    """Parse issue markdown file and extract title, body, and labels."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Extract title from frontmatter
    title_match = re.search(r"title:\s*['\"](.+?)['\"]", content)
    if title_match:
        title = title_match.group(1)
    else:
        # Fallback to first heading
        heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = heading_match.group(1) if heading_match else Path(filepath).stem

    # Extract labels from frontmatter
    labels_match = re.search(r"labels:\s*\[(.+?)\]", content)
    if labels_match:
        labels = [l.strip().strip("'\"") for l in labels_match.group(1).split(",")]
    else:
        labels = ["class-validation", "testing", "refactor", "priority-low"]

    # Remove frontmatter from body
    body = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

    return title, body.strip(), labels


from dotenv import load_dotenv

load_dotenv()


def main():
    # Get GitHub token from environment
    token = os.getenv("GH_TOKEN")
    if not token:
        print("❌ Error: GH_TOKEN environment variable not set")
        print("\nSet it with:")
        print('  $env:GH_TOKEN = "your-github-token"  # PowerShell')
        print('  export GH_TOKEN="your-github-token"   # Bash')
        return

    # Initialize GitHub client
    try:
        g = Github(token)
        repo = g.get_repo("jaewilson07/dl-remuxed")
    except Exception as e:
        print(f"❌ Error connecting to GitHub: {e}")
        return

    # Find issue files
    issues_dir = Path(__file__).parent.parent / "EXPORTS" / "issues"
    issue_files = sorted(issues_dir.glob("issue_*.md"))

    print(f"📁 Found {len(issue_files)} issue files to process\n")

    # Create issues
    created = []
    skipped = []
    failed = []

    for issue_file in issue_files:
        title, body, labels = parse_issue_file(issue_file)

        try:
            # Check if issue already exists
            existing = list(repo.get_issues(state="all"))
            if any(issue.title == title for issue in existing):
                skipped.append((issue_file.name, title))
                print(f"⏭️  Skipped (exists): {title}")
                continue

            # Create the issue
            issue = repo.create_issue(title=title, body=body, labels=labels)
            created.append((issue.number, title, issue.html_url))
            print(f"✅ Created issue #{issue.number}: {title}")

        except Exception as e:
            failed.append((issue_file.name, title, str(e)))
            print(f"❌ Failed: {title} - {e}")

    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary:")
    print(f"   ✅ Created: {len(created)}")
    print(f"   ⏭️  Skipped: {len(skipped)}")
    print(f"   ❌ Failed: {len(failed)}")

    if created:
        print("\n🎉 Created Issues:")
        for num, title, url in created:
            print(f"   #{num}: {title}")
            print(f"          {url}")

    if failed:
        print("\n⚠️  Failed Issues:")
        for filename, title, error in failed:
            print(f"   {filename}: {error}")


if __name__ == "__main__":
    main()
