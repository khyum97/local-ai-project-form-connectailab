#!/usr/bin/env python3
# version: compliance_check_v1
"""Create a general business compliance checklist."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "compliance_check.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text).strip("-").lower() or "system"


def main():
    c = load_config()
    project = os.path.expanduser((c.get("PROJECT_PATH") or os.getcwd()).strip())
    name = (c.get("SYSTEM_NAME") or "Business System").strip()
    out_dir = os.path.join(project, "docs", "legal")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slugify(name)}_compliance_check.md")
    body = f"""# Compliance Checklist: {name}

## Consumer And User Protection
- [ ] User-facing claims are accurate and not misleading.
- [ ] Pricing, refunds, limitations, and cancellation terms are clear.
- [ ] Users can contact support and resolve disputes.

## Operational Controls
- [ ] Critical actions are logged with timestamp, actor, and reason.
- [ ] Approval gates exist for high-risk actions.
- [ ] Manual override and incident response steps are documented.

## Data And Privacy
- [ ] API keys are encrypted or stored in the platform secret store.
- [ ] Personal data collection is minimized and documented.
- [ ] Logs do not expose account numbers, access tokens, or secrets.

## Regulatory Review
- [ ] Applicable industry, consumer, privacy, tax, and labor rules are reviewed.
- [ ] Marketing copy avoids regulated claims unless properly licensed.
- [ ] Terms, privacy policy, disclaimers, and contracts are reviewed by counsel.
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
