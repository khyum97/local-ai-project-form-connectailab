#!/usr/bin/env python3
# version: sprint_planner_v1
"""Create a sprint planning markdown file."""
import datetime as dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "sprint_planner.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def items(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in str(value or "").splitlines() if x.strip()]


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower() or "sprint"


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    name = (cfg.get("SPRINT_NAME") or "Sprint").strip()
    goals = items(cfg.get("GOALS")) or ["Define sprint goal"]
    team = items(cfg.get("TEAM")) or ["senior_dev", "frontend", "backend", "qa"]
    out_dir = os.path.join(project, "docs", "sprints")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{dt.date.today().strftime('%Y%m%d')}_{slugify(name)}.md")
    goal_lines = "\n".join(f"- {g}" for g in goals)
    rows = "\n".join(f"| {member} | TBD | TBD | planned |" for member in team)
    body = f"""# {name}

- Start: {dt.date.today().isoformat()}
- Status: planned

## Goals
{goal_lines}

## Work Plan
| Owner | Task | Acceptance Criteria | Status |
|---|---|---|---|
{rows}

## Risks
-

## Review Plan
- [ ] Build passes
- [ ] Tests pass
- [ ] Release notes updated
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
