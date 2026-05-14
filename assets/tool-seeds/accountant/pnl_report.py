#!/usr/bin/env python3
# version: pnl_report_v1
"""Summarize business transaction CSV profit and loss."""
import csv
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "pnl_report.json")


def cfg():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    c = cfg()
    path = os.path.expanduser((c.get("CSV_FILE") or "").strip())
    if not path:
        raise SystemExit("CSV_FILE is required")
    fee_col = c.get("FEE_COLUMN") or "fee"
    totals = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0, "fee": 0.0})
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            category = row.get("category") or row.get("account") or row.get("symbol") or "Uncategorized"
            kind = (row.get("type") or row.get("side") or "").lower()
            amount = float(row.get("amount") or 0)
            fee = float(row.get(fee_col) or 0)
            if kind in ("revenue", "income", "sale", "credit"):
                totals[category]["revenue"] += amount
            elif kind in ("expense", "cost", "debit", "buy"):
                totals[category]["expense"] += amount
            elif kind == "fee":
                totals[category]["fee"] += amount
            else:
                totals[category]["revenue" if amount >= 0 else "expense"] += abs(amount)
            totals[category]["fee"] += fee
    lines = ["# P&L Report", "", "| Category | Revenue | Expense | Fees | Net Profit |", "|---|---:|---:|---:|---:|"]
    grand = 0.0
    for category, t in sorted(totals.items()):
        pnl = t["revenue"] - t["expense"] - t["fee"]
        grand += pnl
        lines.append(f"| {category} | {t['revenue']:.2f} | {t['expense']:.2f} | {t['fee']:.2f} | {pnl:.2f} |")
    lines += ["", f"**Total net profit:** {grand:.2f}"]
    body = "\n".join(lines) + "\n"
    out = c.get("OUTPUT_FILE")
    if out:
        with open(os.path.expanduser(out), "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
    print(body)


if __name__ == "__main__":
    main()
