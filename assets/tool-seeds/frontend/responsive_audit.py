#!/usr/bin/env python3
# version: responsive_audit_v1
"""반응형 CSS 점검 — 고정 픽셀·overflow·반응형 prefix 누락 패턴 스캔.

config:
  PROJECT_PATH — 스캔할 프로젝트 루트
"""
import os, sys, json, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "responsive_audit.json")

PATTERNS = [
    ("고정 px 너비 (큰 값)", re.compile(r'width:\s*([1-9]\d{2,})px')),
    ("고정 px 높이 (큰 값)", re.compile(r'height:\s*([1-9]\d{2,})px')),
    ("overflow-x hidden", re.compile(r'overflow-x:\s*hidden')),
    ("Tailwind w-\d+ 반응형 prefix 없음", re.compile(r'(?<![:\w])w-(?:96|80|72|64|56|48)')),
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

def _scan_file(path):
    issues = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, 1):
                for label, pat in PATTERNS:
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

    exts = ["**/*.css", "**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.ts"]
    files = []
    for pat in exts:
        files += glob.glob(os.path.join(project, "src", pat), recursive=True)
    files = [f for f in files if "node_modules" not in f]

    _log(f"스캔 대상: {len(files)}개 파일", "info")
    all_issues = []
    for f in files:
        issues = _scan_file(f)
        if issues:
            rel = os.path.relpath(f, project)
            all_issues.append((rel, issues))

    print()
    print("# 🎯 반응형 감사 결과")
    print()
    if not all_issues:
        print("✅ 이슈 없음 — 반응형 패턴 양호")
        return
    total = sum(len(v) for _, v in all_issues)
    print(f"**{total}개 이슈 감지** ({len(all_issues)}개 파일)\n")
    for rel, issues in all_issues:
        print(f"## `{rel}`")
        for line_no, label, snippet in issues:
            print(f"- L{line_no} — **{label}**: `{snippet}`")
        print()
    print("> 각 이슈를 확인하고 반응형 처리를 추가하세요.")

if __name__ == "__main__":
    main()
