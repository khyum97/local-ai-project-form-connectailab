#!/usr/bin/env python3
# version: stack_audit_v1
"""프로젝트 기술 스택 분석 — 의존성 목록·버전 패턴·분류 리포트.

config:
  PROJECT_PATH — 분석할 프로젝트 루트
"""
import os, sys, json, re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "stack_audit.json")

KNOWN_DEPRECATED = ["request", "node-uuid", "jade", "coffee-script", "bower", "grunt", "gulp"]
KNOWN_HEAVY = ["moment", "lodash", "jquery", "underscore"]


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


def _parse_pkg(project):
    pkg_path = os.path.join(project, "package.json")
    if not os.path.exists(pkg_path):
        return None, {}, {}
    pkg = _load(pkg_path)
    return (
        pkg.get("name", os.path.basename(project)),
        pkg.get("dependencies") or {},
        pkg.get("devDependencies") or {},
    )


def _parse_requirements(project):
    req_path = os.path.join(project, "requirements.txt")
    if not os.path.exists(req_path):
        return []
    deps = []
    with open(req_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                deps.append(line)
    return deps


def _version_flag(ver):
    if ver.startswith("^"):
        return "⚠️ 마이너 고정"
    if ver.startswith("~"):
        return "⚠️ 패치 고정"
    if ver.startswith("*") or ver == "latest":
        return "❌ 버전 미고정"
    return "✅ 고정"


def _dep_table(deps, label):
    if not deps:
        return f"### {label}\n\n(없음)\n"
    rows = []
    warnings = []
    for name, ver in sorted(deps.items()):
        flag = _version_flag(ver)
        deprecated = "🚫 deprecated 의심" if name.lower() in KNOWN_DEPRECATED else ""
        heavy = "📦 번들 크기 주의" if name.lower() in KNOWN_HEAVY else ""
        note = " ".join(filter(None, [deprecated, heavy]))
        rows.append(f"| `{name}` | `{ver}` | {flag} | {note or '—'} |")
        if deprecated or heavy:
            warnings.append(f"- `{name}`: {note}")
    table = f"### {label}\n\n| 패키지 | 버전 | 버전 고정 | 비고 |\n|--------|------|-----------|------|\n" + "\n".join(rows) + "\n"
    return table, warnings


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)

    name, deps, dev_deps = _parse_pkg(project)
    py_deps = _parse_requirements(project)

    sections = []
    all_warnings = []

    if name:
        _log(f"Node 프로젝트: {name}", "info")
        t1, w1 = _dep_table(deps, "런타임 의존성 (dependencies)")
        t2, w2 = _dep_table(dev_deps, "개발 의존성 (devDependencies)")
        sections += [t1, t2]
        all_warnings += w1 + w2

    if py_deps:
        _log(f"Python 의존성: {len(py_deps)}개", "info")
        rows = "\n".join(f"| `{d}` |" for d in py_deps)
        sections.append(f"### Python (requirements.txt)\n\n| 패키지 |\n|--------|\n{rows}\n")

    if not sections:
        _log("package.json 도 requirements.txt 도 없음", "warn")

    warn_section = ""
    if all_warnings:
        warn_section = "\n## ⚠️ 주요 경고\n\n" + "\n".join(all_warnings) + "\n"

    total = len(deps) + len(dev_deps) + len(py_deps)
    content = f"""# 🔍 스택 감사 리포트{f" — {name}" if name else ""}

> 분석일: {date.today().isoformat()} | 총 의존성: {total}개

{chr(10).join(sections)}
{warn_section}
## 권고사항

- TODO: 버전 미고정 패키지를 특정 버전으로 고정하세요
- TODO: deprecated 패키지 대체재 검토하세요
- `npm audit` 실행으로 보안 취약점을 별도 확인하세요
"""

    out_dir = os.path.join(project, "docs", "research")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "stack-audit.md")
    _log(f"저장 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"# ✅ 스택 감사 완료")
    print()
    if name:
        print(f"**프로젝트**: {name}")
    print(f"**총 의존성**: {total}개 (런타임 {len(deps)} + 개발 {len(dev_deps)} + Python {len(py_deps)})")
    print(f"**경고**: {len(all_warnings)}개")
    print(f"**파일**: `{out_path}`")
    if all_warnings:
        print()
        print("주요 경고:")
        for w in all_warnings:
            print(w)


if __name__ == "__main__":
    main()
