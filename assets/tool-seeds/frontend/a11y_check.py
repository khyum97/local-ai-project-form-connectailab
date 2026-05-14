#!/usr/bin/env python3
# version: a11y_check_v1
"""접근성 정적 점검 — img alt / button label / input label 누락 스캔.

config:
  PROJECT_PATH — 스캔할 프로젝트 루트
"""
import os, sys, json, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "a11y_check.json")

CHECKS = [
    ("img alt 누락", re.compile(r'<img(?![^>]*\balt\s*=)[^>]*/?>',  re.IGNORECASE)),
    ("button 텍스트·aria-label 없음", re.compile(r'<button(?![^>]*aria-label)[^>]*>\s*</button>', re.IGNORECASE)),
    ("input aria-label / htmlFor 없음", re.compile(r'<input(?![^>]*(?:aria-label|id\s*=))[^>]*/?>',  re.IGNORECASE)),
    ("tabIndex 음수", re.compile(r'tabIndex\s*=\s*[{"]?-\d+')),
    ("role 없는 div onClick", re.compile(r'<div[^>]+onClick[^>]*(?!role=)[^>]*>')),
]

def _log(msg, kind="info"):
    prefix = {"info": "🎯", "ok": "✅", "warn": "⚠️ ", "err": "❌"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)

def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _scan(path):
    issues = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, 1):
                for label, pat in CHECKS:
                    if pat.search(line):
                        issues.append((i, label, line.strip()[:80]))
    except Exception:
        pass
    return issues

def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)

    files = []
    for pat in ["**/*.tsx", "**/*.jsx", "**/*.html"]:
        files += glob.glob(os.path.join(project, "src", pat), recursive=True)
    files = [f for f in files if "node_modules" not in f]

    _log(f"스캔: {len(files)}개 파일", "info")
    all_issues = []
    for f in files:
        iss = _scan(f)
        if iss:
            all_issues.append((os.path.relpath(f, project), iss))

    print()
    print("# 🎯 접근성 점검 결과")
    print()
    if not all_issues:
        print("✅ 이슈 없음 — 기본 접근성 항목 양호")
        return
    total = sum(len(v) for _, v in all_issues)
    print(f"**{total}개 이슈** ({len(all_issues)}개 파일)\n")
    for rel, issues in all_issues:
        print(f"## `{rel}`")
        for ln, label, snippet in issues:
            print(f"- L{ln} — **{label}**: `{snippet}`")
        print()
    print("> WCAG 2.1 AA 기준으로 위 항목을 수정하세요.")

if __name__ == "__main__":
    main()
