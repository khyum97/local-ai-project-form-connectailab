#!/usr/bin/env python3
# version: bug_report_v1
"""Create a standard bug report markdown file.

config:
  PROJECT_PATH  project root where docs/bugs will be created
  BUG_TITLE     report title
  SEVERITY      critical|high|medium|low
  ENVIRONMENT   runtime/environment note
"""
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "bug_report.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower()
    return slug or "bug-report"


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    title = (cfg.get("BUG_TITLE") or "Untitled bug").strip()
    severity = (cfg.get("SEVERITY") or "medium").strip().lower()
    env = (cfg.get("ENVIRONMENT") or "TBD").strip()

    out_dir = os.path.join(project, "docs", "bugs")
    os.makedirs(out_dir, exist_ok=True)
    today = dt.date.today().strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"{today}_{slugify(title)}.md")

    body = f"""# Bug Report: {title}

- Severity: {severity}
- Environment: {env}
- Reported: {dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
- Status: open

## Summary
Describe the problem in one or two sentences.

## Steps To Reproduce
1.
2.
3.

## Expected Result

## Actual Result

## Evidence
- Logs:
- Screenshots:
- Related commits/issues:

## Impact

## Fix Notes

## Verification
- [ ] Reproduced
- [ ] Fixed
- [ ] Regression test added
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
