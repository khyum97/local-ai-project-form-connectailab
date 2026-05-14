#!/usr/bin/env python3
# version: tax_calc_v1
"""Estimate business tax."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "tax_calc.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    c = load_config()
    income = float(c.get("INCOME") or c.get("GAIN") or 0)
    deduction = float(c.get("DEDUCTION") or 0)
    rate = float(c.get("TAX_RATE") or 0.22)
    taxable = max(0.0, income - deduction)
    tax = taxable * rate
    print("# Tax Estimate")
    print()
    print(f"- Income/profit: {income:,.2f}")
    print(f"- Deduction: {deduction:,.2f}")
    print(f"- Taxable gain: {taxable:,.2f}")
    print(f"- Tax rate: {rate:.2%}")
    print(f"- Estimated tax: {tax:,.2f}")
    print()
    print("> This is an estimate. Confirm current tax rules with a licensed tax professional.")


if __name__ == "__main__":
    main()
