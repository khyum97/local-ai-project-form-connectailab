#!/usr/bin/env python3
# version: component_scaffold_v1
"""React/TypeScript 컴포넌트 보일러플레이트 생성기.

지아가 새 React 컴포넌트를 만들 때 호출:
  1. COMPONENT_NAME + TYPE + CSS_MODE 읽어 .tsx 파일 생성
  2. Props 인터페이스 + 기본 구조 포함
  3. OUTPUT_DIR 없으면 자동 생성

config (component_scaffold.json):
  COMPONENT_NAME — PascalCase 컴포넌트 이름 (예: UserCard)
  TYPE           — 'function' (기본) | 'forwardRef'
  CSS_MODE       — 'tailwind' (기본) | 'module' | 'plain'
  OUTPUT_DIR     — 출력 폴더 경로 (예: src/components)
"""
import os, sys, json


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "component_scaffold.json")


def _log(msg, kind="info"):
    prefix = {"info": "🧩", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _css_snippet(css_mode, name):
    if css_mode == "tailwind":
        return '  <div className="flex flex-col">\n    {children}\n  </div>'
    elif css_mode == "module":
        return f'  <div className={{styles.wrapper}}>\n    {{children}}\n  </div>'
    else:
        return '  <div>\n    {children}\n  </div>'


def _module_import(css_mode, name):
    if css_mode == "module":
        return f"import styles from './{name}.module.css';\n"
    return ""


def _build_function_template(name, css_mode):
    css_import = _module_import(css_mode, name)
    body = _css_snippet(css_mode, name)
    return f"""\
import React from 'react';
{css_import}
export interface {name}Props {{
  children?: React.ReactNode;
  className?: string;
}}

export function {name}({{ children, className }}: {name}Props) {{
  return (
{body}
  );
}}

export default {name};
"""


def _build_forward_ref_template(name, css_mode):
    css_import = _module_import(css_mode, name)
    body = _css_snippet(css_mode, name)
    return f"""\
import React from 'react';
{css_import}
export interface {name}Props {{
  children?: React.ReactNode;
  className?: string;
}}

export const {name} = React.forwardRef<HTMLDivElement, {name}Props>(
  ({{ children, className }}, ref) => {{
    return (
      <div ref={{ref}}>
{body}
      </div>
    );
  }}
);

{name}.displayName = '{name}';
export default {name};
"""


def main():
    cfg = _load(CONFIG)

    name = (cfg.get("COMPONENT_NAME") or "").strip()
    if not name:
        _log("COMPONENT_NAME 이 비어 있습니다.", "err")
        sys.exit(1)

    comp_type = (cfg.get("TYPE") or "function").strip().lower()
    css_mode = (cfg.get("CSS_MODE") or "tailwind").strip().lower()
    output_dir = (cfg.get("OUTPUT_DIR") or "").strip()

    if not output_dir:
        _log("OUTPUT_DIR 이 비어 있습니다.", "err")
        sys.exit(1)

    output_dir = os.path.expanduser(output_dir)
    out_file = os.path.join(output_dir, f"{name}.tsx")

    # 이미 존재하면 덮어쓰지 않음
    if os.path.exists(out_file):
        _log(f"파일이 이미 존재합니다: {out_file}", "warn")
        _log("덮어쓰지 않고 종료합니다. 파일을 삭제 후 재실행하세요.", "warn")
        sys.exit(1)

    # 폴더 생성
    os.makedirs(output_dir, exist_ok=True)
    _log(f"출력 폴더: {output_dir}", "step")

    # 템플릿 선택
    if comp_type == "forwardref":
        content = _build_forward_ref_template(name, css_mode)
    else:
        content = _build_function_template(name, css_mode)

    # 파일 작성
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    _log(f"생성 완료: {out_file}", "ok")

    # 결과 리포트
    print()
    print(f"# 🧩 component_scaffold 결과")
    print()
    print(f"- **컴포넌트**: `{name}`")
    print(f"- **타입**: `{comp_type}`")
    print(f"- **CSS 방식**: `{css_mode}`")
    print(f"- **출력 파일**: `{out_file}`")
    print()
    print("## 생성된 파일 내용")
    print()
    print("```tsx")
    print(content)
    print("```")


if __name__ == "__main__":
    main()
