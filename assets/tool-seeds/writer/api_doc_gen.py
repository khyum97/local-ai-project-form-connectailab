#!/usr/bin/env python3
# version: api_doc_gen_v1
"""API 문서 자동 생성 — 라우트 파일 파싱 후 마크다운 레퍼런스 생성.

config:
  PROJECT_PATH — 프로젝트 루트
  SOURCE_FILE  — 라우트 소스 파일 (예: src/routes/users.ts)
  API_PREFIX   — 경로 prefix (예: /api/v1)
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "api_doc_gen.json")

METHOD_COLORS = {"GET": "🟢", "POST": "🔵", "PUT": "🟡", "PATCH": "🟠", "DELETE": "🔴"}


def _log(msg, kind="info"):
    prefix = {"info": "📝", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _parse_routes(src_text):
    routes = []
    # Express: router.get('/path', ...) or app.post('/path', ...)
    express = re.findall(
        r'(?:router|app)\.(get|post|put|patch|delete)\s*\(\s*[\'"`]([^\'"` ]+)[\'"`]',
        src_text, re.IGNORECASE
    )
    for method, path in express:
        routes.append((method.upper(), path))
    # FastAPI: @app.get("/path") or @router.post("/path")
    fastapi = re.findall(
        r'@(?:app|router)\.(get|post|put|patch|delete)\s*\(\s*[\'"`]([^\'"` ]+)[\'"`]',
        src_text, re.IGNORECASE
    )
    for method, path in fastapi:
        if (method.upper(), path) not in routes:
            routes.append((method.upper(), path))
    return routes


def _build_doc(routes, file_name, prefix):
    if not routes:
        return f"# 📝 {file_name} API\n\n> 라우트를 자동으로 감지하지 못했습니다. 수동으로 작성하세요.\n"

    sections = [f"# 📝 {file_name} API 레퍼런스\n", f"> Base path: `{prefix or '/'}`\n"]
    for method, path in routes:
        icon = METHOD_COLORS.get(method, "⚪")
        full_path = prefix + path if prefix else path
        sections.append(f"\n## {icon} {method} `{full_path}`\n")
        sections.append("**설명**: TODO\n")
        sections.append("\n**요청 파라미터**\n")
        sections.append("| 위치 | 이름 | 타입 | 필수 | 설명 |\n")
        sections.append("|------|------|------|------|------|\n")
        sections.append("| — | — | — | — | TODO |\n")
        sections.append("\n**응답**\n")
        sections.append("```json\n// TODO: 응답 스키마\n```\n")
    return "".join(sections)


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    source = (cfg.get("SOURCE_FILE") or "").strip()
    if not source:
        _log("SOURCE_FILE 이 설정되지 않음", "err")
        sys.exit(1)
    prefix = (cfg.get("API_PREFIX") or "").strip().rstrip("/")

    src_abs = os.path.join(project, source) if not os.path.isabs(source) else source
    if not os.path.exists(src_abs):
        _log(f"소스 파일 없음: {src_abs}", "err")
        sys.exit(1)

    _log(f"라우트 파싱: {src_abs}", "info")
    with open(src_abs, "r", encoding="utf-8", errors="ignore") as f:
        src_text = f.read()

    routes = _parse_routes(src_text)
    _log(f"감지된 라우트: {len(routes)}개", "ok" if routes else "warn")

    file_name = os.path.splitext(os.path.basename(source))[0]
    doc = _build_doc(routes, file_name, prefix)

    out_dir = os.path.join(project, "docs", "api")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{file_name}.md")

    _log(f"저장 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)

    print()
    print(f"# ✅ API 문서 생성 완료")
    print()
    print(f"**소스**: `{source}`")
    print(f"**감지된 엔드포인트**: {len(routes)}개")
    print(f"**파일**: `{out_path}`")
    print()
    if routes:
        for method, path in routes:
            icon = METHOD_COLORS.get(method, "⚪")
            print(f"- {icon} {method} {prefix + path if prefix else path}")
    print()
    print("> TODO 항목에 파라미터·응답 스키마를 채워 완성하세요.")


if __name__ == "__main__":
    main()
