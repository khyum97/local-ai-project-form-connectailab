#!/usr/bin/env python3
# version: lib_compare_v1
"""라이브러리 비교 리포트 마크다운 생성.

npm registry API 로 주간 다운로드·버전 조회 시도.
네트워크 실패 시 TODO 로 대체.

config:
  PROJECT_PATH — 프로젝트 루트
  TOPIC        — 비교 주제 (파일명으로 사용)
  CANDIDATES   — 비교할 라이브러리들 (쉼표 구분)
  CRITERIA     — 비교 기준 (쉼표 구분)
"""
import os, sys, json, urllib.request, urllib.error
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "lib_compare.json")

DEFAULT_CRITERIA = ["번들크기", "학습곡선", "생태계", "TypeScript지원", "유지보수"]


def _log(msg, kind="info"):
    prefix = {"info": "🔍", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _npm_info(pkg):
    try:
        url = f"https://registry.npmjs.org/{pkg}/latest"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
            version = data.get("version", "?")
        dl_url = f"https://api.npmjs.org/downloads/point/last-week/{pkg}"
        with urllib.request.urlopen(dl_url, timeout=5) as r:
            dl = json.loads(r.read()).get("downloads", "?")
        return version, f"{dl:,}" if isinstance(dl, int) else str(dl)
    except Exception:
        return "?", "?"


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    topic = (cfg.get("TOPIC") or "comparison").strip().lower().replace(" ", "-")
    raw_candidates = (cfg.get("CANDIDATES") or "").strip()
    if not raw_candidates:
        _log("CANDIDATES 비어있음 — lib_compare.json 에 작성하세요", "err")
        sys.exit(1)
    candidates = [c.strip() for c in raw_candidates.split(",") if c.strip()]
    raw_criteria = (cfg.get("CRITERIA") or "").strip()
    criteria = [c.strip() for c in raw_criteria.split(",") if c.strip()] if raw_criteria else DEFAULT_CRITERIA

    _log(f"비교 대상: {', '.join(candidates)}", "info")

    # npm 정보 조회
    info = {}
    for c in candidates:
        _log(f"npm 조회: {c}", "step")
        ver, dl = _npm_info(c)
        info[c] = {"version": ver, "downloads": dl}

    # 매트릭스 헤더
    header = "| 기준 | " + " | ".join(candidates) + " |"
    sep = "|------|" + "------|" * len(candidates)
    rows = []
    for cr in criteria:
        cells = " | ".join("TODO" for _ in candidates)
        rows.append(f"| {cr} | {cells} |")

    # 버전/다운로드 행
    ver_cells = " | ".join(info[c]["version"] for c in candidates)
    dl_cells = " | ".join(info[c]["downloads"] for c in candidates)

    content = f"""# 🔍 라이브러리 비교 — {topic}

> 생성일: {date.today().isoformat()} | 비교 대상: {', '.join(f'`{c}`' for c in candidates)}

## 버전 및 인기도

| 항목 | {' | '.join(candidates)} |
|------|{'------|' * len(candidates)}
| 최신 버전 | {ver_cells} |
| 주간 다운로드 | {dl_cells} |

## 비교 매트릭스

{header}
{sep}
{chr(10).join(rows)}

> 각 셀에 ⭐⭐⭐ (우수) / ⭐⭐ (보통) / ⭐ (미흡) 또는 수치로 채우세요.

## 결론

**추천**: TODO — 위 매트릭스를 채운 후 결론 작성

**근거**:
- TODO

**비추천 이유**:
- TODO

## 참고 링크

{chr(10).join(f'- [{c}](https://www.npmjs.com/package/{c})' for c in candidates)}
"""

    out_dir = os.path.join(project, "docs", "research")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{topic}.md")
    _log(f"저장 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"# ✅ 라이브러리 비교 리포트 생성 완료")
    print()
    print(f"**주제**: {topic}")
    print(f"**비교 대상**: {', '.join(candidates)}")
    print(f"**파일**: `{out_path}`")
    print()
    print("> TODO 셀을 채워 비교 매트릭스를 완성하세요.")


if __name__ == "__main__":
    main()
