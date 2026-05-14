#!/usr/bin/env python3
# version: contract_template_v1
"""Create a service terms template."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "contract_template.json")


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
    service = (c.get("SERVICE_NAME") or "Business Service").strip()
    party = (c.get("PARTY_NAME") or "[Customer]").strip()
    out_dir = os.path.join(project, "docs", "legal")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slugify(service)}_terms_template.md")
    body = f"""# Service Terms Template: {service}

Parties: {service} and {party}

## 1. Scope
The service provides software tools, workflow automation, data processing, reporting, and operational support.

## 2. User Obligations
The user must maintain brokerage account credentials, comply with applicable laws, and review automated settings before use.

## 3. Fees
Fees, billing cycle, taxes, refunds, and late payment terms are defined in the applicable order form.

## 4. Risk And Disclaimers
The user acknowledges market risk, technology risk, and the possibility of financial loss.

## 5. Data Protection
Each party will protect confidential information and personal data according to applicable law and the privacy policy.

## 6. Limitation Of Liability
Liability exclusions and caps must be reviewed under governing law before use.

## 7. Term And Termination
Either party may terminate according to the notice period stated in the order form.

## 8. Governing Law
Governing law and venue: [TBD].
"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
