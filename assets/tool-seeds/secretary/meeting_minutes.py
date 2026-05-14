#!/usr/bin/env python3
# version: meeting_minutes_v1
"""Create a meeting minutes markdown template."""
import datetime as dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "meeting_minutes.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower() or "meeting"


def split_items(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in re.split(r"[,\n]", str(value or "")) if x.strip()]


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    title = (cfg.get("MEETING_TITLE") or "Meeting").strip()
    attendees = split_items(cfg.get("ATTENDEES"))
    out_dir = os.path.join(project, "docs", "meetings")
    os.makedirs(out_dir, exist_ok=True)
    today = dt.date.today().strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"{today}_{slugify(title)}.md")
    attendee_lines = "\n".join(f"- {name}" for name in attendees) if attendees else "- TBD"
    body = f"""# {title}

- Date: {dt.date.today().isoformat()}
- Facilitator: TBD

## Attendees
{attendee_lines}

## Agenda
1.
2.

## Decisions
-

## Action Items
| Owner | Task | Due | Status |
|---|---|---|---|
| TBD | TBD | TBD | open |

## Notes

"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
