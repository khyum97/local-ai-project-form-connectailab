#!/usr/bin/env python3
# version: disclaimer_gen_v1
"""Create a service disclaimer draft."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "disclaimer_gen.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower() or "service"


def main():
    c = load_config()
    project = os.path.expanduser((c.get("PROJECT_PATH") or os.getcwd()).strip())
    name = (c.get("SERVICE_NAME") or "Business Service").strip()
    out_dir = os.path.join(project, "docs", "legal")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slugify(name)}_disclaimer.md")
    body = f"""# Legal Disclaimer: {name}

This document is a draft and must be reviewed by qualified counsel before use.

## No Professional Advice
The service provides software, data processing, automation, and workflow support. It does not provide personalized legal, tax, accounting, financial, medical, or other regulated professional advice.

## Risk Disclosure
Business decisions, automation, integrations, and third-party services involve operational, financial, legal, and technical risk. Users are responsible for reviewing outputs before relying on them.

## No Guaranteed Results
Backtests, simulations, examples, and historical performance do not guarantee future results.

## User Responsibility
Users are responsible for reviewing outputs, configuring limits, monitoring activity, and complying with applicable laws, platform terms, and internal policies.

## System Availability
The service may be interrupted by network failures, exchange outages, brokerage API changes, software defects, or maintenance.
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
