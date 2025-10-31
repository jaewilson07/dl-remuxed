#!/usr/bin/env python3
"""
Script to capture all comments from a GitHub Pull Request and save them to a ToDo.md file.

Usage:
    python capture_pr_comments.py --pr 178 --token YOUR_GITHUB_TOKEN

Or set environment variable:
    export GITHUB_TOKEN=your_token_here
    python capture_pr_comments.py --pr 178
"""

import argparse
import os
from datetime import datetime
from typing import Any

import requests


class GitHubPRCommentCapture:
    def __init__(
        self, token: str, owner: str = "jaewilson07", repo: str = "dl-remuxed"
    ):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_pr_info(self, pr_number: int) -> dict[str, Any]:
        """Get basic PR information"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pr_comments(self, pr_number: int) -> list[dict[str, Any]]:
        """Get all issue comments (general PR comments)"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{pr_number}/comments"
        comments = []
        page = 1

        while True:
            response = requests.get(
                url, headers=self.headers, params={"page": page, "per_page": 100}
            )
            response.raise_for_status()
            page_comments = response.json()

            if not page_comments:
                break

            comments.extend(page_comments)
            page += 1

        return comments

    def get_review_comments(self, pr_number: int) -> list[dict[str, Any]]:
        """Get all review comments (line-specific comments)"""
        url = (
            f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/comments"
        )
        comments = []
        page = 1

        while True:
            response = requests.get(
                url, headers=self.headers, params={"page": page, "per_page": 100}
            )
            response.raise_for_status()
            page_comments = response.json()

            if not page_comments:
                break

            comments.extend(page_comments)
            page += 1

        return comments

    def get_reviews(self, pr_number: int) -> list[dict[str, Any]]:
        """Get all PR reviews"""
        url = (
            f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/reviews"
        )
        reviews = []
        page = 1

        while True:
            response = requests.get(
                url, headers=self.headers, params={"page": page, "per_page": 100}
            )
            response.raise_for_status()
            page_reviews = response.json()

            if not page_reviews:
                break

            reviews.extend(page_reviews)
            page += 1

        return reviews

    def format_datetime(self, iso_string: str) -> str:
        """Format ISO datetime string to readable format"""
        try:
            dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return iso_string

    def generate_todo_markdown(self, pr_number: int) -> str:
        """Generate markdown content for ToDo.md file"""
        print(f"Fetching PR #{pr_number} information...")
        pr_info = self.get_pr_info(pr_number)

        print("Fetching PR comments...")
        pr_comments = self.get_pr_comments(pr_number)

        print("Fetching review comments...")
        review_comments = self.get_review_comments(pr_number)

        print("Fetching reviews...")
        reviews = self.get_reviews(pr_number)

        # Start building markdown
        markdown_lines = []
        markdown_lines.append(f"# ToDo Items from PR #{pr_number}")
        markdown_lines.append("")
        markdown_lines.append(f"**PR Title:** {pr_info['title']}")
        markdown_lines.append(f"**PR URL:** {pr_info['html_url']}")
        markdown_lines.append(f"**Status:** {pr_info['state']}")
        markdown_lines.append(
            f"**Created:** {self.format_datetime(pr_info['created_at'])}"
        )
        markdown_lines.append(
            f"**Updated:** {self.format_datetime(pr_info['updated_at'])}"
        )
        markdown_lines.append("")

        if pr_info.get("body"):
            markdown_lines.append("## PR Description")
            markdown_lines.append("")
            markdown_lines.append(pr_info["body"])
            markdown_lines.append("")

        # Add general PR comments
        if pr_comments:
            markdown_lines.append("## General Comments")
            markdown_lines.append("")

            for comment in sorted(pr_comments, key=lambda x: x["created_at"]):
                author = comment["user"]["login"]
                created = self.format_datetime(comment["created_at"])
                body = comment["body"]

                markdown_lines.append(f"### Comment by @{author}")
                markdown_lines.append(f"**Date:** {created}")
                markdown_lines.append("")
                markdown_lines.append(body)
                markdown_lines.append("")
                markdown_lines.append("---")
                markdown_lines.append("")

        # Add reviews
        if reviews:
            markdown_lines.append("## Reviews")
            markdown_lines.append("")

            for review in sorted(
                reviews, key=lambda x: x["submitted_at"] or x["created_at"]
            ):
                author = review["user"]["login"]
                state = review["state"]
                submitted = self.format_datetime(
                    review["submitted_at"] or review["created_at"]
                )

                markdown_lines.append(f"### Review by @{author} - {state}")
                markdown_lines.append(f"**Date:** {submitted}")
                markdown_lines.append("")

                if review.get("body"):
                    markdown_lines.append(review["body"])
                    markdown_lines.append("")

                markdown_lines.append("---")
                markdown_lines.append("")

        # Add review comments (line-specific)
        if review_comments:
            markdown_lines.append("## Code Review Comments")
            markdown_lines.append("")

            # Group by file
            comments_by_file = {}
            for comment in review_comments:
                file_path = comment.get("path", "Unknown file")
                if file_path not in comments_by_file:
                    comments_by_file[file_path] = []
                comments_by_file[file_path].append(comment)

            for file_path, comments in comments_by_file.items():
                markdown_lines.append(f"### File: `{file_path}`")
                markdown_lines.append("")

                for comment in sorted(comments, key=lambda x: x["created_at"]):
                    author = comment["user"]["login"]
                    created = self.format_datetime(comment["created_at"])
                    line = comment.get("line", comment.get("original_line", "Unknown"))
                    body = comment["body"]

                    markdown_lines.append(f"**@{author}** (Line {line}) - {created}")
                    markdown_lines.append("")
                    markdown_lines.append(body)
                    markdown_lines.append("")

                markdown_lines.append("---")
                markdown_lines.append("")

        # Add summary section
        markdown_lines.append("## Action Items Summary")
        markdown_lines.append("")
        markdown_lines.append("### 🔍 Items to Review")
        markdown_lines.append("- [ ] Review all comments above")
        markdown_lines.append("- [ ] Address code review feedback")
        markdown_lines.append("- [ ] Update documentation as needed")
        markdown_lines.append("")

        markdown_lines.append("### 📝 Next Steps")
        markdown_lines.append("- [ ] Prioritize action items")
        markdown_lines.append("- [ ] Create GitHub issues for major items")
        markdown_lines.append("- [ ] Schedule implementation")
        markdown_lines.append("")

        markdown_lines.append("---")
        markdown_lines.append(
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )

        return "\n".join(markdown_lines)

    def save_to_file(self, content: str, filename: str = "ToDo.md"):
        """Save content to file"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"ToDo items saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Capture GitHub PR comments to ToDo.md"
    )
    parser.add_argument("--pr", type=int, required=True, help="PR number to capture")
    parser.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--owner", default="jaewilson07", help="Repository owner")
    parser.add_argument("--repo", default="dl-remuxed", help="Repository name")
    parser.add_argument("--output", default="ToDo.md", help="Output filename")

    args = parser.parse_args()

    # Get token from argument or environment
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print(
            "Error: GitHub token required. Use --token or set GITHUB_TOKEN environment variable."
        )
        print("You can create a token at: https://github.com/settings/tokens")
        return 1

    try:
        capture = GitHubPRCommentCapture(token, args.owner, args.repo)
        content = capture.generate_todo_markdown(args.pr)
        capture.save_to_file(content, args.output)
        print(f"Successfully captured comments from PR #{args.pr}")
        return 0

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Invalid GitHub token or insufficient permissions.")
        elif e.response.status_code == 404:
            print(f"Error: PR #{args.pr} not found or repository not accessible.")
        else:
            print(f"Error: HTTP {e.response.status_code} - {e.response.text}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
