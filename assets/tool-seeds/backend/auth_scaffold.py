#!/usr/bin/env python3
# version: auth_scaffold_v1
"""JWT 인증 뼈대 생성 — Express 또는 FastAPI.

config:
  PROJECT_PATH — 프로젝트 루트
  FRAMEWORK    — 'express' | 'fastapi' (기본 express)
  SECRET_ENV   — JWT secret 환경변수명 (기본 JWT_SECRET)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "auth_scaffold.json")

EXPRESS_MIDDLEWARE = '''import {{ Request, Response, NextFunction }} from 'express';
import jwt from 'jsonwebtoken';

const SECRET = process.env.{secret} || 'change-me';

export interface AuthRequest extends Request {{
  userId?: string;
}}

export function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {{
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) {{
    return res.status(401).json({{ error: 'Unauthorized' }});
  }}
  try {{
    const payload = jwt.verify(header.slice(7), SECRET) as {{ userId: string }};
    req.userId = payload.userId;
    next();
  }} catch {{
    return res.status(401).json({{ error: 'Invalid token' }});
  }}
}}

export function generateToken(userId: string): string {{
  return jwt.sign({{ userId }}, SECRET, {{ expiresIn: '24h' }});
}}
'''

EXPRESS_ROUTE = '''import {{ Router, Request, Response }} from 'express';
import {{ generateToken }} from '../middleware/auth';

const router = Router();

// POST /auth/login
router.post('/login', async (req: Request, res: Response) => {{
  const {{ email, password }} = req.body;
  // TODO: DB에서 사용자 조회 및 비밀번호 검증
  const userId = 'TODO';
  const token = generateToken(userId);
  res.json({{ token }});
}});

// POST /auth/register
router.post('/register', async (req: Request, res: Response) => {{
  // TODO: DB에 사용자 등록
  res.status(201).json({{ message: 'registered' }});
}});

export default router;
'''

FASTAPI_JWT = '''from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

SECRET_KEY = os.getenv("{secret}", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

bearer = HTTPBearer()

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({{"sub": user_id, "exp": expire}}, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    try:
        payload = jwt.decode(cred.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
'''

FASTAPI_ROUTER = '''from fastapi import APIRouter, Depends
from .jwt import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(email: str, password: str):
    # TODO: DB에서 사용자 조회 및 비밀번호 검증
    token = create_access_token(user_id="TODO")
    return {{"access_token": token, "token_type": "bearer"}}

@router.post("/register", status_code=201)
async def register(email: str, password: str):
    # TODO: DB에 사용자 등록
    return {{"message": "registered"}}

@router.get("/me")
async def me(user_id: str = Depends(get_current_user)):
    return {{"user_id": user_id}}
'''

def _log(msg, kind="info"):
    prefix = {"info": "⚙️", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)

def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    fw = (cfg.get("FRAMEWORK") or "express").strip().lower()
    secret = (cfg.get("SECRET_ENV") or "JWT_SECRET").strip()

    created = []
    if fw == "express":
        pairs = [
            (os.path.join(project, "src", "middleware", "auth.ts"), EXPRESS_MIDDLEWARE.format(secret=secret)),
            (os.path.join(project, "src", "routes", "auth.ts"), EXPRESS_ROUTE.format(secret=secret)),
        ]
    elif fw == "fastapi":
        pairs = [
            (os.path.join(project, "app", "auth", "jwt.py"), FASTAPI_JWT.format(secret=secret)),
            (os.path.join(project, "app", "auth", "router.py"), FASTAPI_ROUTER.format(secret=secret)),
        ]
    else:
        _log(f"지원하지 않는 프레임워크: {fw}", "err")
        sys.exit(1)

    for path, content in pairs:
        if os.path.exists(path):
            _log(f"이미 존재 — 건너뜀: {path}", "warn")
            continue
        _log(f"생성: {path}", "step")
        _write(path, content)
        created.append(path)

    print()
    print("# ✅ 인증 뼈대 생성 완료")
    print(f"\n**프레임워크**: {fw} | **JWT_SECRET 환경변수**: `{secret}`\n")
    for p in created:
        print(f"- `{os.path.relpath(p, project)}`")
    print("\n> TODO 주석 위치에 DB 연동 코드를 작성하세요.")

if __name__ == "__main__":
    main()
