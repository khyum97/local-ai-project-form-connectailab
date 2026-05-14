#!/usr/bin/env python3
# version: daily_report_gen_v1
"""Create a daily report markdown file."""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "daily_report_gen.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def lines(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in str(value or "").splitlines() if x.strip()]


def section(title, items):
    body = "\n".join(f"- {item}" for item in items) if items else "- None"
    return f"## {title}\n{body}\n"


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    out_dir = os.path.join(project, "docs", "reports")
    os.makedirs(out_dir, exist_ok=True)
    today = dt.date.today().strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"{today}_daily_report.md")
    body = f"""# Daily Report - {dt.date.today().isoformat()}

{section("Completed", lines(cfg.get("COMPLETED")))}
{section("Planned", lines(cfg.get("PLANNED")))}
{section("Blockers", lines(cfg.get("BLOCKERS")))}
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
