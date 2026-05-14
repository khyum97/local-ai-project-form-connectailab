#!/usr/bin/env python3
# version: comment_gen_v1
"""Add lightweight JSDoc/docstring stubs to uncommented functions.

config:
  SOURCE_FILE  .ts, .tsx, .js, or .py source file
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "comment_gen.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def add_ts_comments(text):
    pattern = re.compile(r"(^\s*)(export\s+)?(async\s+)?function\s+([A-Za-z0-9_]+)\s*\(", re.MULTILINE)

    def repl(match):
        start = match.start()
        prev = text[max(0, start - 120):start]
        if "/**" in prev:
            return match.group(0)
        indent = match.group(1)
        name = match.group(4)
        return f"{indent}/**\n{indent} * TODO: Document {name}.\n{indent} */\n{match.group(0)}"

    return pattern.sub(repl, text)


def add_py_comments(text):
    pattern = re.compile(r"(^\s*)def\s+([A-Za-z0-9_]+)\s*\([^)]*\):\s*$", re.MULTILINE)

    def repl(match):
        end = match.end()
        following = text[end:end + 80]
        if '"""' in following or "'''" in following:
            return match.group(0)
        indent = match.group(1)
        name = match.group(2)
        body_indent = indent + "    "
        return f'{match.group(0)}\n{body_indent}"""TODO: Document {name}."""'

    return pattern.sub(repl, text)


def main():
    cfg = load_config()
    src = os.path.expanduser((cfg.get("SOURCE_FILE") or "").strip())
    if not src or not os.path.exists(src):
        raise SystemExit("SOURCE_FILE is required")
    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    if src.endswith(".py"):
        out = add_py_comments(text)
        out_path = src[:-3] + ".commented.py"
    else:
        out = add_ts_comments(text)
        root, ext = os.path.splitext(src)
        out_path = root + ".commented" + ext
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
