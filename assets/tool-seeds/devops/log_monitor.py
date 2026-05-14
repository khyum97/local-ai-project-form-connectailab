#!/usr/bin/env python3
# version: log_monitor_v1
"""로그 파일 에러/경고 패턴 분석 — 스냅샷 요약 리포트.

config:
  LOG_FILE   — 단일 로그 파일 (우선)
  LOG_DIR    — 로그 디렉토리 (최신 .log 파일 자동 선택)
  TAIL_LINES — 미리보기 줄 수 (기본 20)
"""
import os, sys, json, re, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "log_monitor.json")

LEVEL_PATS = {
    "ERROR": re.compile(r'\b(ERROR|error|Error)\b'),
    "WARN":  re.compile(r'\b(WARN|WARNING|warn|warning)\b'),
    "FATAL": re.compile(r'\b(FATAL|CRITICAL|fatal|critical)\b'),
}

def _log(msg, kind="info"):
    prefix = {"info": "🚀", "ok": "✅", "warn": "⚠️ ", "err": "❌"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)

def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    cfg = _load(CONFIG)
    log_file = (cfg.get("LOG_FILE") or "").strip()
    log_dir  = (cfg.get("LOG_DIR") or "").strip()
    tail     = int(cfg.get("TAIL_LINES") or 20)

    if log_file:
        target = os.path.expanduser(log_file)
    elif log_dir:
        files = sorted(glob.glob(os.path.join(os.path.expanduser(log_dir), "**/*.log"), recursive=True), key=os.path.getmtime, reverse=True)
        if not files:
            _log("LOG_DIR 에서 .log 파일 없음", "err")
            sys.exit(1)
        target = files[0]
    else:
        _log("LOG_FILE 또는 LOG_DIR 설정 필요", "err")
        sys.exit(1)

    if not os.path.exists(target):
        _log(f"파일 없음: {target}", "err")
        sys.exit(1)

    _log(f"분석: {target}", "info")
    with open(target, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    counts = {lvl: 0 for lvl in LEVEL_PATS}
    error_msgs = []
    for line in lines:
        for lvl, pat in LEVEL_PATS.items():
            if pat.search(line):
                counts[lvl] += 1
                if lvl in ("ERROR", "FATAL"):
                    clean = line.strip()[:120]
                    error_msgs.append(clean)

    top_errors = Counter(error_msgs).most_common(5)
    tail_lines = lines[-tail:]

    print()
    print(f"# 🚀 로그 분석 — `{os.path.basename(target)}`")
    print(f"\n**총 줄**: {len(lines):,} | **ERROR**: {counts['ERROR']} | **WARN**: {counts['WARN']} | **FATAL**: {counts['FATAL']}\n")

    if top_errors:
        print("## 반복 에러 TOP 5\n")
        for msg, cnt in top_errors:
            print(f"- ({cnt}회) `{msg}`")
        print()

    print(f"## 최근 {tail}줄\n```")
    for l in tail_lines:
        print(l.rstrip())
    print("```")

if __name__ == "__main__":
    main()
