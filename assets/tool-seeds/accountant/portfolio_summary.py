#!/usr/bin/env python3
# version: portfolio_summary_v1
"""Create a portfolio summary from holdings CSV."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "portfolio_summary.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    c = load_config()
    path = os.path.expanduser((c.get("CSV_FILE") or "").strip())
    if not path:
        raise SystemExit("CSV_FILE is required")
    rows = []
    total_value = 0.0
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            symbol = row.get("symbol") or row.get("ticker") or "UNKNOWN"
            qty = float(row.get("quantity") or row.get("qty") or 0)
            avg = float(row.get("avg_price") or row.get("average_price") or 0)
            current = float(row.get("current_price") or row.get("price") or avg)
            cost = qty * avg
            value = qty * current
            total_value += value
            rows.append((symbol, qty, avg, current, cost, value, value - cost))
    lines = ["# Portfolio Summary", "", "| Symbol | Qty | Avg | Current | Value | P&L | Allocation |", "|---|---:|---:|---:|---:|---:|---:|"]
    for symbol, qty, avg, current, _cost, value, pnl in rows:
        alloc = (value / total_value * 100) if total_value else 0
        lines.append(f"| {symbol} | {qty:.4f} | {avg:.2f} | {current:.2f} | {value:.2f} | {pnl:.2f} | {alloc:.2f}% |")
    lines += ["", f"**Total value:** {total_value:.2f}"]
    body = "\n".join(lines) + "\n"
    out = c.get("OUTPUT_FILE")
    if out:
        with open(os.path.expanduser(out), "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
    print(body)


if __name__ == "__main__":
    main()
