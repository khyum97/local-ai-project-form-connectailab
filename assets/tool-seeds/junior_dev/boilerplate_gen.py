#!/usr/bin/env python3
# version: boilerplate_gen_v1
"""보일러플레이트 파일 자동 생성 — 템플릿 선택 후 즉시 파일 생성.

연아가 새 모듈 시작 전 호출하면:
  1. TEMPLATE_TYPE 에 따라 파일 내용·이름 결정
  2. OUTPUT_DIR 에 파일 생성
  3. 생성된 파일 절대 경로 출력

config:
  TEMPLATE_TYPE — 'util-function' | 'hook' | 'service' | 'config'
  NAME          — 파일/심볼 이름 (예: formatDate, Auth, database)
  OUTPUT_DIR    — 파일 생성 디렉터리 경로
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "boilerplate_gen.json")


def _log(msg, kind="info"):
    prefix = {"info": "🏗️ ", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _pascal(name):
    return name[0].upper() + name[1:] if name else name


def _camel(name):
    return name[0].lower() + name[1:] if name else name


def _util_template(name):
    camel = _camel(name)
    return f"""/**
 * {camel} — TODO: 함수 설명 작성
 */
export function {camel}(input: unknown): unknown {{
  // TODO: 구현
  throw new Error('{camel} is not implemented');
}}

export default {camel};
"""


def _hook_template(name):
    pascal = _pascal(name)
    hook_name = f"use{pascal}"
    return f"""import {{ useState, useEffect }} from 'react';

interface {pascal}State {{
  data: unknown;
  loading: boolean;
  error: Error | null;
}}

/**
 * {hook_name} — TODO: 훅 설명 작성
 */
export function {hook_name}(): {pascal}State {{
  const [data, setData] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {{
    // TODO: 비동기 로직 구현
  }}, []);

  return {{ data, loading, error }};
}}

export default {hook_name};
"""


def _service_template_full(name):
    pascal = _pascal(name)
    return f"""/**
 * {pascal}Service — TODO: 서비스 설명 작성
 */
export class {pascal}Service {{
  constructor() {{
    // TODO: 의존성 주입
  }}

  async getAll(): Promise<unknown[]> {{
    // TODO: 구현
    throw new Error('getAll is not implemented');
  }}

  async getById(id: string): Promise<unknown> {{
    // TODO: 구현
    throw new Error('getById is not implemented');
  }}

  async create(data: unknown): Promise<unknown> {{
    // TODO: 구현
    throw new Error('create is not implemented');
  }}

  async update(id: string, data: unknown): Promise<unknown> {{
    // TODO: 구현
    throw new Error('update is not implemented');
  }}

  async delete(id: string): Promise<void> {{
    // TODO: 구현
    throw new Error('delete is not implemented');
  }}
}}

export default {pascal}Service;
"""


def _config_json_template(name):
    return json.dumps({
        "name": name,
        "version": "1.0.0",
        "settings": {
            "debug": False,
            "logLevel": "info",
            "timeout": 30
        }
    }, ensure_ascii=False, indent=2) + "\n"


def _config_env_template(name):
    upper = name.upper()
    return f"""# {name} 설정 — 실제 값으로 교체 후 .env 로 복사
{upper}_API_KEY=your_api_key_here
{upper}_API_URL=https://api.example.com
{upper}_TIMEOUT=30
{upper}_DEBUG=false
NODE_ENV=development
"""


def main():
    cfg = _load(CONFIG)

    template_type = (cfg.get("TEMPLATE_TYPE") or "").strip().lower()
    name = (cfg.get("NAME") or "").strip()
    output_dir = (cfg.get("OUTPUT_DIR") or "").strip()

    if not template_type:
        _log("TEMPLATE_TYPE 이 설정되지 않음 (util-function|hook|service|config)", "err")
        sys.exit(1)
    if template_type not in ("util-function", "hook", "service", "config"):
        _log(f"지원하지 않는 템플릿: {template_type}", "err")
        sys.exit(1)
    if not name:
        _log("NAME 이 설정되지 않음", "err")
        sys.exit(1)
    if not output_dir:
        _log("OUTPUT_DIR 이 설정되지 않음", "err")
        sys.exit(1)

    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    _log(f"템플릿: {template_type} | 이름: {name} | 출력: {output_dir}", "info")

    created = []

    if template_type == "util-function":
        filename = f"{_camel(name)}.ts"
        out_path = os.path.join(output_dir, filename)
        content = _util_template(name)
        files_to_write = [(out_path, content)]

    elif template_type == "hook":
        pascal = _pascal(name)
        filename = f"use{pascal}.ts"
        out_path = os.path.join(output_dir, filename)
        content = _hook_template(name)
        files_to_write = [(out_path, content)]

    elif template_type == "service":
        pascal = _pascal(name)
        filename = f"{pascal}Service.ts"
        out_path = os.path.join(output_dir, filename)
        content = _service_template_full(name)
        files_to_write = [(out_path, content)]

    else:  # config
        lower = name.lower()
        json_path = os.path.join(output_dir, f"{lower}.json")
        env_path = os.path.join(output_dir, ".env.example")
        files_to_write = [
            (json_path, _config_json_template(name)),
            (env_path, _config_env_template(name)),
        ]

    for out_path, content in files_to_write:
        if os.path.exists(out_path):
            _log(f"파일 이미 존재 — 건너뜀: {out_path}", "warn")
            continue
        _log(f"생성: {out_path}", "step")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        created.append(out_path)

    print()
    print(f"# 🏗️ 보일러플레이트 생성 완료 — {template_type}")
    print()
    print(f"**이름**: `{name}`")
    print(f"**출력 디렉터리**: `{output_dir}`")
    print()

    if created:
        print(f"## ✅ 생성된 파일 ({len(created)}개)")
        for p in created:
            print(f"- `{p}`")
        print()
        print("> TODO 주석 위치에 실제 로직을 구현하세요.")
    else:
        print("## ⚠️ 생성된 파일 없음 — 모든 대상 파일이 이미 존재합니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
