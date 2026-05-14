#!/usr/bin/env python3
# version: readme_gen_v1
"""README.md 자동 생성 — package.json + 폴더 구조 기반 초안.

config:
  PROJECT_PATH — 프로젝트 루트
  LANG         — 'ko' | 'en' (기본 ko)
"""
import os, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "readme_gen.json")


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


def _scan_src(project):
    src = os.path.join(project, "src")
    if not os.path.isdir(src):
        return []
    entries = []
    for item in sorted(os.listdir(src)):
        full = os.path.join(src, item)
        if os.path.isdir(full):
            sub = sorted(os.listdir(full))[:5]
            entries.append(f"├── {item}/")
            for s in sub:
                entries.append(f"│   └── {s}")
        else:
            entries.append(f"├── {item}")
    return entries


def _build_ko(name, description, version, scripts, structure):
    scripts_md = "\n".join(f"| `npm run {k}` | `{v}` |" for k, v in scripts.items()) if scripts else "| (없음) | — |"
    structure_md = "\n".join(structure) if structure else "(src/ 폴더 없음)"
    return f"""# {name}

> {description or "TODO: 프로젝트 설명 작성"}

**버전**: `{version}`

---

## 개요

TODO: 이 프로젝트가 해결하는 문제와 주요 기능을 설명하세요.

## 설치

```bash
npm install
```

## 사용법

```bash
npm run dev
```

TODO: 사용 예시와 스크린샷을 추가하세요.

## 스크립트

| 명령 | 내용 |
|------|------|
{scripts_md}

## 프로젝트 구조

```
src/
{structure_md}
```

## 기여

Pull Request 환영합니다. 큰 변경은 Issue를 먼저 열어 논의하세요.

## 라이선스

[MIT](LICENSE)
"""


def _build_en(name, description, version, scripts, structure):
    scripts_md = "\n".join(f"| `npm run {k}` | `{v}` |" for k, v in scripts.items()) if scripts else "| (none) | — |"
    structure_md = "\n".join(structure) if structure else "(no src/ folder)"
    return f"""# {name}

> {description or "TODO: describe this project"}

**Version**: `{version}`

---

## Overview

TODO: describe what problem this project solves and its key features.

## Installation

```bash
npm install
```

## Usage

```bash
npm run dev
```

TODO: add usage examples and screenshots.

## Scripts

| Command | Description |
|---------|-------------|
{scripts_md}

## Project Structure

```
src/
{structure_md}
```

## Contributing

PRs are welcome. For major changes, open an issue first.

## License

[MIT](LICENSE)
"""


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    lang = (cfg.get("LANG") or "ko").strip().lower()

    pkg_path = os.path.join(project, "package.json")
    pkg = _load(pkg_path)
    name = pkg.get("name") or os.path.basename(project)
    description = pkg.get("description") or ""
    version = pkg.get("version") or "0.0.1"
    scripts = {k: v for k, v in (pkg.get("scripts") or {}).items() if k not in ("postinstall", "prepare")}

    structure = _scan_src(project)
    _log(f"프로젝트: {name} v{version}", "info")

    content = _build_ko(name, description, version, scripts, structure) if lang == "ko" else _build_en(name, description, version, scripts, structure)

    readme_path = os.path.join(project, "README.md")
    draft_path = os.path.join(project, "README.draft.md")

    if os.path.exists(readme_path):
        _log(f"README.md 이미 존재 → README.draft.md 로 저장", "warn")
        out_path = draft_path
    else:
        out_path = readme_path

    _log(f"저장 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"# ✅ README 생성 완료")
    print()
    print(f"**프로젝트**: {name} v{version}")
    print(f"**언어**: {lang}")
    print(f"**파일**: `{out_path}`")
    print()
    print("> `TODO` 항목을 채워 README를 완성하세요.")


if __name__ == "__main__":
    main()
