#!/usr/bin/env python3
# version: util_scaffold_v1
"""Create a small TypeScript utility module.

config:
  PROJECT_PATH  project root
  UTIL_TYPE     date|string|number|http
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "util_scaffold.json")

TEMPLATES = {
    "date": """export function formatDate(value: Date | string | number): string {
  const date = value instanceof Date ? value : new Date(value);
  return date.toISOString().slice(0, 10);
}

export function daysBetween(a: Date, b: Date): number {
  const ms = b.getTime() - a.getTime();
  return Math.round(ms / 86400000);
}
""",
    "string": """export function toTitleCase(value: string): string {
  return value
    .trim()
    .split(/\\s+/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

export function truncate(value: string, maxLength = 80): string {
  return value.length <= maxLength ? value : `${value.slice(0, maxLength - 1)}...`;
}
""",
    "number": """export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

export function formatCurrency(value: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
}
""",
    "http": """export async function getJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}
""",
}


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    kind = (cfg.get("UTIL_TYPE") or "string").strip().lower()
    if kind not in TEMPLATES:
        raise SystemExit(f"Unsupported UTIL_TYPE: {kind}")
    out_dir = os.path.join(project, "src", "utils")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{kind}.ts")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEMPLATES[kind])
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
