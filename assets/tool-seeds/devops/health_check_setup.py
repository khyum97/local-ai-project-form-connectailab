#!/usr/bin/env python3
# version: health_check_setup_v1
"""헬스체크 엔드포인트 뼈대 생성.

config:
  PROJECT_PATH — 프로젝트 루트
  FRAMEWORK    — 'express' | 'fastapi' | 'nginx' (기본 express)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "health_check_setup.json")

EXPRESS = """import { Router, Request, Response } from 'express';

const router = Router();
const START = Date.now();

router.get('/health', async (_req: Request, res: Response) => {
  const uptime = Math.floor((Date.now() - START) / 1000);
  // TODO: DB 연결 체크 추가
  res.json({
    status: 'ok',
    uptime_sec: uptime,
    version: process.env.npm_package_version ?? 'unknown',
    timestamp: new Date().toISOString(),
  });
});

export default router;
"""

FASTAPI = """from fastapi import APIRouter
import time, os

router = APIRouter(tags=["health"])
_START = time.time()

@router.get("/health")
async def health():
    # TODO: DB 연결 체크 추가
    return {
        "status": "ok",
        "uptime_sec": int(time.time() - _START),
        "version": os.getenv("APP_VERSION", "unknown"),
    }
"""

NGINX = """# nginx health check endpoint
location /health {
    access_log off;
    return 200 '{"status":"ok"}';
    add_header Content-Type application/json;
}
"""

TEMPLATES = {"express": EXPRESS, "fastapi": FASTAPI, "nginx": NGINX}
PATHS = {
    "express": ("src", "routes", "health.ts"),
    "fastapi": ("app", "health.py"),
    "nginx": ("nginx", "health.conf"),
}

def _log(msg, kind="info"):
    prefix = {"info": "🚀", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    fw = (cfg.get("FRAMEWORK") or "express").strip().lower()
    if fw not in TEMPLATES:
        _log(f"지원하지 않는 프레임워크: {fw}", "err")
        sys.exit(1)

    rel_parts = PATHS[fw]
    out_path = os.path.join(project, *rel_parts)
    if os.path.exists(out_path):
        _log(f"이미 존재 — 건너뜀: {out_path}", "warn")
        sys.exit(0)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    _log(f"생성: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATES[fw])

    print()
    print("# ✅ 헬스체크 설정 생성 완료")
    print(f"\n**프레임워크**: {fw}")
    print(f"**파일**: `{os.path.relpath(out_path, project)}`")
    print("\n> TODO 주석에 DB 연결 체크 코드를 추가하세요.")

if __name__ == "__main__":
    main()
