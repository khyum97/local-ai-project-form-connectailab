#!/usr/bin/env python3
# version: dockerfile_gen_v1
"""Dockerfile + .dockerignore 자동 생성 도구.

서준이 APP_TYPE에 따라 최적 Dockerfile을 생성한다:
  - node   : node:20-alpine 멀티스테이지 (빌드 + 런타임 분리)
  - python : python:3.12-slim, pip install requirements.txt
  - static : nginx:alpine, 정적 파일 서빙

config (dockerfile_gen.json):
  PROJECT_PATH — 프로젝트 루트 (필수)
  APP_TYPE     — 'node' | 'python' | 'static' (필수)
  PORT         — 노출 포트 (기본 3000)
  BASE_IMAGE   — 베이스 이미지 오버라이드 (선택)
  OUTPUT_PATH  — 출력 경로 (기본 PROJECT_PATH)
"""
import os, sys, json


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "dockerfile_gen.json")


def _log(msg, kind="info"):
    prefix = {"info": "🐳", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def _dockerfile_node(port, base_image):
    base = base_image or "node:20-alpine"
    return f"""# syntax=docker/dockerfile:1
FROM {base} AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

FROM {base} AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build --if-present

FROM {base} AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
EXPOSE {port}
CMD ["node", "dist/index.js"]
"""


def _dockerfile_python(port, base_image):
    base = base_image or "python:3.12-slim"
    return f"""# syntax=docker/dockerfile:1
FROM {base}
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE {port}
CMD ["python", "main.py"]
"""


def _dockerfile_static(base_image):
    base = base_image or "nginx:alpine"
    return f"""# syntax=docker/dockerfile:1
FROM {base}
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""


def _dockerignore_node():
    return """node_modules
dist
.git
.gitignore
*.log
.env*
coverage
.nyc_output
"""


def _dockerignore_python():
    return """__pycache__
*.pyc
*.pyo
.venv
venv
.git
.gitignore
*.log
.env*
dist
build
"""


def _dockerignore_static():
    return """.git
.gitignore
*.log
.env*
node_modules
"""


def main():
    cfg = _load(CONFIG)

    project = (cfg.get("PROJECT_PATH") or "").strip()
    if not project:
        _log("PROJECT_PATH 설정 필요", "err")
        sys.exit(1)
    project = os.path.expanduser(project)
    if not os.path.isdir(project):
        _log(f"폴더 없음: {project}", "err")
        sys.exit(1)

    app_type = (cfg.get("APP_TYPE") or "").strip().lower()
    if app_type not in ("node", "python", "static"):
        _log("APP_TYPE 은 'node' | 'python' | 'static' 중 하나여야 함", "err")
        sys.exit(1)

    port = str(cfg.get("PORT") or "3000").strip()
    base_image = (cfg.get("BASE_IMAGE") or "").strip() or None
    output_path = (cfg.get("OUTPUT_PATH") or "").strip() or project
    output_path = os.path.expanduser(output_path)

    _log(f"타입: {app_type} | 포트: {port} | 출력: {output_path}", "info")

    if app_type == "node":
        dockerfile = _dockerfile_node(port, base_image)
        dockerignore = _dockerignore_node()
    elif app_type == "python":
        dockerfile = _dockerfile_python(port, base_image)
        dockerignore = _dockerignore_python()
    else:
        dockerfile = _dockerfile_static(base_image)
        dockerignore = _dockerignore_static()

    df_path = os.path.join(output_path, "Dockerfile")
    di_path = os.path.join(output_path, ".dockerignore")

    _write(df_path, dockerfile)
    _log(f"Dockerfile 생성: {df_path}", "ok")

    _write(di_path, dockerignore)
    _log(f".dockerignore 생성: {di_path}", "ok")

    print()
    print(f"# 🐳 Dockerfile 생성 완료 — {app_type}")
    print()
    print(f"| 항목 | 값 |")
    print(f"|------|----|")
    print(f"| APP_TYPE | `{app_type}` |")
    print(f"| BASE_IMAGE | `{base_image or '기본값'}` |")
    print(f"| PORT | `{port}` |")
    print(f"| Dockerfile | `{df_path}` |")
    print(f"| .dockerignore | `{di_path}` |")
    print()
    print("> 다음 단계: `docker build -t myapp .` 로 빌드 확인")


if __name__ == "__main__":
    main()
