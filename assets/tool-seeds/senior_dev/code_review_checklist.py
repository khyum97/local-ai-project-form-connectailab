#!/usr/bin/env python3
# version: code_review_checklist_v1
"""Create a code review checklist markdown file."""
import datetime as dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "code_review_checklist.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower() or "review"


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    title = (cfg.get("PR_TITLE") or "Code Review").strip()
    out_dir = os.path.join(project, "docs", "reviews")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{dt.date.today().strftime('%Y%m%d')}_{slugify(title)}_checklist.md")
    body = f"""# Code Review Checklist: {title}

## Correctness
- [ ] Requirements are implemented.
- [ ] Edge cases and failure paths are handled.
- [ ] Public APIs and data contracts remain compatible.

## Tests
- [ ] Unit or integration tests cover changed behavior.
- [ ] Manual verification steps are documented.
- [ ] No flaky or environment-dependent assertions were added.

## Security
- [ ] Inputs are validated and encoded.
- [ ] Secrets are not logged or committed.
- [ ] Auth, permissions, and rate limits are preserved.

## Performance
- [ ] No avoidable repeated I/O or expensive loops.
- [ ] Queries and network calls are bounded.
- [ ] Large payloads are streamed or paginated where needed.

## Maintainability
- [ ] Names and structure match the existing codebase.
- [ ] Comments explain non-obvious decisions only.
- [ ] No unrelated refactors are included.
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
