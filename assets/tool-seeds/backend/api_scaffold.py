#!/usr/bin/env python3
# version: api_scaffold_v1
"""REST API 엔드포인트 보일러플레이트 생성 도구.

민준이 새 API 엔드포인트를 설계할 때 이 도구를 호출하면:
  1. FRAMEWORK (express|fastapi) 확인
  2. ENDPOINT + METHOD 기반 라우터 코드 생성
  3. OUTPUT_DIR 에 파일 저장 후 결과 리포트

config:
  FRAMEWORK  — 'express' 또는 'fastapi' (필수)
  ENDPOINT   — API 경로 (예: '/users', '/items/{id}') (필수)
  METHOD     — 'GET'|'POST'|'PUT'|'DELETE' (기본 'GET')
  OUTPUT_DIR — 출력 폴더 (비우면 현재 디렉토리)
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "api_scaffold.json")

ALLOWED_FRAMEWORKS = ("express", "fastapi")
ALLOWED_METHODS = ("GET", "POST", "PUT", "DELETE")


def _log(msg, kind="info"):
    prefix = {"info": "🛠", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _endpoint_to_name(endpoint):
    name = re.sub(r"[^a-zA-Z0-9]", "_", endpoint).strip("_")
    return name or "endpoint"


def _express_template(endpoint, method):
    name = _endpoint_to_name(endpoint)
    method_lower = method.lower()
    has_body = method in ("POST", "PUT")
    body_interface = ""
    body_param = ""
    if has_body:
        body_interface = f"\ninterface {name.capitalize()}Body {{\n  // TODO: 요청 바디 필드 정의\n}}\n"
        body_param = f"\n  const body: {name.capitalize()}Body = req.body;"
    return f"""import {{ Router, Request, Response }} from 'express';

const router = Router();

interface {name.capitalize()}Response {{
  success: boolean;
  data?: unknown;
  message?: string;
}}
{body_interface}
router.{method_lower}('{endpoint}', async (req: Request, res: Response<{name.capitalize()}Response>) => {{
  try {{{body_param}
    // TODO: 비즈니스 로직 구현
    res.json({{ success: true, data: null }});
  }} catch (error) {{
    res.status(500).json({{ success: false, message: String(error) }});
  }}
}});

export default router;
"""


def _fastapi_template(endpoint, method):
    name = _endpoint_to_name(endpoint)
    method_lower = method.lower()
    has_body = method in ("POST", "PUT")
    body_import = ""
    body_model = ""
    body_param = ""
    if has_body:
        body_import = "from pydantic import BaseModel\n"
        body_model = f"\n\nclass {name.capitalize()}Request(BaseModel):\n    pass  # TODO: 요청 바디 필드 정의\n"
        body_param = f", body: {name.capitalize()}Request"
    return f"""from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
{body_import}
router = APIRouter()
{body_model}

class {name.capitalize()}Response(BaseModel):
    success: bool
    data: object | None = None
    message: str | None = None


@router.{method_lower}('{endpoint}', response_model={name.capitalize()}Response)
async def {method_lower}_{name}({body_param.lstrip(', ')}):
    try:
        # TODO: 비즈니스 로직 구현
        return {name.capitalize()}Response(success=True, data=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""


def main():
    cfg = _load(CONFIG)

    framework = (cfg.get("FRAMEWORK") or "").strip().lower()
    endpoint = (cfg.get("ENDPOINT") or "").strip()
    method = (cfg.get("METHOD") or "GET").strip().upper()
    output_dir = (cfg.get("OUTPUT_DIR") or "").strip() or os.getcwd()

    if framework not in ALLOWED_FRAMEWORKS:
        _log(f"FRAMEWORK 값 오류: '{framework}'. 허용: {ALLOWED_FRAMEWORKS}", "err")
        sys.exit(1)
    if not endpoint:
        _log("ENDPOINT 비어있음 (예: '/users')", "err")
        sys.exit(1)
    if method not in ALLOWED_METHODS:
        _log(f"METHOD 값 오류: '{method}'. 허용: {ALLOWED_METHODS}", "err")
        sys.exit(1)
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            _log(f"OUTPUT_DIR 생성: {output_dir}", "step")
        except Exception as e:
            _log(f"OUTPUT_DIR 생성 실패: {e}", "err")
            sys.exit(1)

    _log(f"프레임워크: {framework}", "info")
    _log(f"엔드포인트: {method} {endpoint}", "info")

    if framework == "express":
        code = _express_template(endpoint, method)
        out_file = os.path.join(output_dir, "router.ts")
    else:
        code = _fastapi_template(endpoint, method)
        out_file = os.path.join(output_dir, "router.py")

    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(code)
        _log(f"파일 저장: {out_file}", "ok")
    except Exception as e:
        _log(f"파일 저장 실패: {e}", "err")
        sys.exit(1)

    print()
    print(f"# 🛠 api_scaffold 결과")
    print()
    print(f"**프레임워크**: `{framework}`")
    print(f"**엔드포인트**: `{method} {endpoint}`")
    print(f"**생성 파일**: `{out_file}`")
    print()
    print("```")
    print(code.strip())
    print("```")
    print()
    print("> ✅ 보일러플레이트 생성 완료. TODO 항목 채워서 사용.")


if __name__ == "__main__":
    main()
