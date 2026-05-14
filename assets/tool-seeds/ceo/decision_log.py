#!/usr/bin/env python3
# version: decision_log_v1
"""기술 결정 기록 — decisions.md 에 결정 사항 누적 저장.

CEO가 아키텍처·기술 방향 결정 후 호출하면:
  1. 타임스탬프 + 제목 + 내용 + 대안 블록 생성
  2. _shared/decisions.md 상단에 prepend

config:
  BRAIN_PATH       — 두뇌 폴더 경로 (기본 ~/.connect-ai-brain)
  DECISION_TITLE   — 결정 제목
  DECISION_BODY    — 결정 내용 및 근거
  ALTERNATIVES     — 검토한 대안들 (쉼표 구분, 없으면 빈 문자열)
"""
import os, sys, json
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "decision_log.json")


def _log(msg, kind="info"):
    prefix = {"info": "🧭", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
    brain = os.path.expanduser((cfg.get("BRAIN_PATH") or "~/.connect-ai-brain").strip())
    title = (cfg.get("DECISION_TITLE") or "").strip()
    body = (cfg.get("DECISION_BODY") or "").strip()
    alternatives = (cfg.get("ALTERNATIVES") or "").strip()

    if not title:
        _log("DECISION_TITLE 비어있음 — decision_log.json 에 작성하세요", "err")
        sys.exit(1)
    if not body:
        _log("DECISION_BODY 비어있음", "err")
        sys.exit(1)

    shared_dir = os.path.join(brain, "_shared")
    os.makedirs(shared_dir, exist_ok=True)
    decisions_path = os.path.join(shared_dir, "decisions.md")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    alt_lines = ""
    if alternatives:
        items = [a.strip() for a in alternatives.split(",") if a.strip()]
        alt_lines = "\n**검토한 대안:**\n" + "\n".join(f"- {a}" for a in items) + "\n"

    new_block = f"""## [{now}] {title}

{body}
{alt_lines}
---

"""

    existing = ""
    if os.path.exists(decisions_path):
        with open(decisions_path, "r", encoding="utf-8") as f:
            existing = f.read()
    else:
        existing = "# 기술 결정 기록\n\n"

    header_end = existing.find("\n\n") + 2 if "\n\n" in existing else len(existing)
    header = existing[:header_end]
    rest = existing[header_end:]

    updated = header + new_block + rest

    _log(f"decisions.md 업데이트: {decisions_path}", "step")
    with open(decisions_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print()
    print("# ✅ 결정 기록 완료")
    print()
    print(f"**제목**: {title}")
    print(f"**시각**: {now}")
    print(f"**저장 위치**: `{decisions_path}`")
    if alternatives:
        print(f"**검토 대안**: {alternatives}")
    print()
    print("> decisions.md 업데이트 완료. Git 자동 동기화로 기록이 보존됩니다.")


if __name__ == "__main__":
    main()
