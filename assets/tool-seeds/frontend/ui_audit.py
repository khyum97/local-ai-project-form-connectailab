#!/usr/bin/env python3
# version: ui_audit_v1
"""프론트엔드 코드 품질 감사 — .tsx/.jsx 파일 스캔 + 이슈 리포트.

지아가 PR 전 또는 코드 리뷰 전 호출:
  1. PROJECT_PATH 하위 .tsx/.jsx 파일 재귀 탐색
  2. aria 누락 / console.log / any 타입 / TODO·FIXME 감사
  3. 파일별 이슈 목록 마크다운 리포트 출력

config (ui_audit.json):
  PROJECT_PATH — 감사할 프로젝트 루트 폴더
  STRICT       — 'true' 면 이슈 시 exit code 1 (CI 연동용). 기본 false
"""
import os, sys, json, re, glob


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "ui_audit.json")


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


# 각 감사 규칙: (규칙 이름, 패턴, 설명)
RULES = [
    ("console.log 잔존",   re.compile(r'console\.log\s*\('),          "디버그 로그 제거 필요"),
    ("any 타입 사용",       re.compile(r':\s*any\b|as\s+any\b'),        "TypeScript any 타입 사용"),
    ("TODO/FIXME 태그",    re.compile(r'//\s*(TODO|FIXME)\b'),          "미완성 작업 태그"),
    ("img alt 누락 의심",  re.compile(r'<img\b(?![^>]*\balt\s*=)[^>]*>'), "img 태그에 alt 속성 없음"),
    ("button label 누락", re.compile(r'<button\b(?![^>]*(?:aria-label|aria-labelledby|title)\s*=)[^>]*>'), "button에 접근성 레이블 없음"),
]


def _audit_file(filepath):
    """파일 하나를 읽어 이슈 목록 반환: [(줄번호, 규칙명, 설명, 줄내용)]"""
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return [(-1, "파일 읽기 오류", str(e), "")]

    for lineno, line in enumerate(lines, start=1):
        for rule_name, pattern, description in RULES:
            if pattern.search(line):
                issues.append((lineno, rule_name, description, line.rstrip()))
    return issues


def main():
    cfg = _load(CONFIG)
    project = (cfg.get("PROJECT_PATH") or "").strip()
    if not project:
        _log("PROJECT_PATH 가 비어 있습니다.", "err")
        sys.exit(1)

    project = os.path.expanduser(project)
    if not os.path.isdir(project):
        _log(f"폴더 없음: {project}", "err")
        sys.exit(1)

    strict = str(cfg.get("STRICT", "")).lower() in ("true", "1", "yes")
    _log(f"감사 대상: {project}", "info")

    # .tsx / .jsx 파일 수집
    patterns = ["**/*.tsx", "**/*.jsx"]
    all_files = []
    for pat in patterns:
        all_files.extend(glob.glob(os.path.join(project, pat), recursive=True))

    # node_modules / dist / .next 제외
    exclude = {"node_modules", "dist", ".next", "build", "out"}
    all_files = [
        f for f in all_files
        if not any(ex in f.replace("\\", "/").split("/") for ex in exclude)
    ]
    all_files = sorted(set(all_files))

    if not all_files:
        _log("검사할 .tsx/.jsx 파일 없음", "warn")
        sys.exit(0)

    _log(f"{len(all_files)}개 파일 감사 시작", "step")

    # 파일별 감사
    file_results = {}  # filepath -> [issues]
    total_issues = 0
    for fp in all_files:
        issues = _audit_file(fp)
        file_results[fp] = issues
        total_issues += len(issues)

    # 마크다운 리포트 출력
    print()
    print(f"# 🔍 ui_audit 결과 — {os.path.basename(project)}")
    print()
    print(f"- 검사 파일 수: **{len(all_files)}**")
    print(f"- 총 이슈 수: **{total_issues}**")
    print()

    if total_issues == 0:
        print("✅ 이슈 없음 — 클린 상태입니다.")
    else:
        print("## 파일별 이슈 목록")
        print()
        for fp, issues in file_results.items():
            if not issues:
                continue
            rel = os.path.relpath(fp, project).replace("\\", "/")
            print(f"### `{rel}` ({len(issues)}개 이슈)")
            print()
            print("| 줄 | 규칙 | 설명 | 코드 |")
            print("|---|---|---|---|")
            for lineno, rule, desc, code in issues:
                code_escaped = code.strip().replace("|", "\\|")[:80]
                print(f"| {lineno} | {rule} | {desc} | `{code_escaped}` |")
            print()

        print()
        if strict:
            _log(f"STRICT 모드: 이슈 {total_issues}개 발견 → exit 1", "err")
            sys.exit(1)
        else:
            print(f"> ⚠️ 총 {total_issues}개 이슈 발견. 위 목록 참고하여 수정하세요.")


if __name__ == "__main__":
    main()
