#!/usr/bin/env python3
# version: task_breakdown_v1
"""작업 분해 및 에이전트 배분 — 큰 작업을 서브태스크로 나누고 담당 에이전트 지정.

CEO가 요청 수신 직후 호출하면:
  1. TASK_DESC 읽기
  2. 키워드 분석으로 담당 에이전트 매핑
  3. 마크다운 테이블 출력

config:
  TASK_DESC    — 분해할 작업 설명 텍스트
  MAX_SUBTASKS — 최대 서브태스크 수 (기본 8)
"""
import os, sys, json, re, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "task_breakdown.json")


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


AGENT_KEYWORDS = {
    "senior_dev": ["아키텍처", "설계", "리팩토링", "성능", "최적화", "디버깅", "구조", "architecture", "refactor", "performance"],
    "frontend": ["UI", "컴포넌트", "화면", "페이지", "버튼", "폼", "레이아웃", "react", "vue", "css", "tailwind"],
    "backend": ["API", "DB", "데이터베이스", "서버", "엔드포인트", "인증", "쿼리", "REST", "sql", "auth"],
    "devops": ["배포", "CI", "CD", "도커", "docker", "쿠버네티스", "kubernetes", "파이프라인", "인프라", "nginx"],
    "designer": ["디자인", "와이어프레임", "UX", "UI설계", "목업", "스펙", "figma", "디자인시스템"],
    "qa": ["테스트", "버그", "검증", "QA", "단위테스트", "E2E", "jest", "playwright", "pytest"],
    "writer": ["문서", "README", "API문서", "주석", "가이드", "changelog", "docs"],
    "researcher": ["조사", "비교", "분석", "트렌드", "라이브러리", "프레임워크", "research", "benchmark"],
    "junior_dev": ["보일러플레이트", "반복", "포맷", "유틸", "boilerplate", "scaffold", "util"],
}

AGENT_LABELS = {
    "senior_dev": "코다리 (시니어)",
    "frontend": "지아 (프론트엔드)",
    "backend": "민준 (백엔드)",
    "devops": "서준 (DevOps)",
    "designer": "Designer (UI/UX)",
    "qa": "유나 (QA)",
    "writer": "Writer (문서)",
    "researcher": "Researcher (조사)",
    "junior_dev": "연아 (주니어)",
    "ceo": "CEO (자체 처리)",
}


def _guess_agent(text: str) -> str:
    text_lower = text.lower()
    scores = {agent: 0 for agent in AGENT_KEYWORDS}
    for agent, kws in AGENT_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in text_lower:
                scores[agent] += 1
    best = max(scores, key=lambda a: scores[a])
    return best if scores[best] > 0 else "senior_dev"


def _split_tasks(desc: str, max_n: int):
    lines = [l.strip() for l in re.split(r"[\n,;·•\-–]", desc) if l.strip()]
    tasks = []
    for line in lines:
        if len(line) < 5:
            continue
        tasks.append(line[:120])
        if len(tasks) >= max_n:
            break
    if not tasks:
        tasks = [textwrap.shorten(desc, width=100, placeholder="...")]
    return tasks


def main():
    cfg = _load(CONFIG)
    task_desc = (cfg.get("TASK_DESC") or "").strip()
    if not task_desc:
        _log("TASK_DESC 비어있음 — task_breakdown.json 에 작성하세요", "err")
        sys.exit(1)
    max_n = int(cfg.get("MAX_SUBTASKS") or 8)
    _log(f"작업 분해 중 (최대 {max_n}개)...", "info")

    subtasks = _split_tasks(task_desc, max_n)
    assignments = [(t, _guess_agent(t)) for t in subtasks]

    print()
    print("# 🧭 작업 분해 결과")
    print()
    print(f"**원본 요청**: {textwrap.shorten(task_desc, width=80, placeholder='...')}")
    print()
    print(f"| # | 서브태스크 | 담당 에이전트 |")
    print(f"|---|------------|--------------|")
    for i, (task, agent) in enumerate(assignments, 1):
        label = AGENT_LABELS.get(agent, agent)
        print(f"| {i} | {task} | {label} |")
    print()
    print(f"> 총 {len(assignments)}개 서브태스크. 순서대로 각 에이전트에 전달하세요.")


if __name__ == "__main__":
    main()
