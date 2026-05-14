#!/usr/bin/env python3
# version: ci_setup_v1
"""GitHub Actions CI 워크플로 자동 생성 도구.

서준이 WORKFLOW_TYPE에 따라 .github/workflows/ci.yml 을 생성한다:
  - node-test    : Node 20, npm ci, npm test
  - python-test  : Python 3.12, pip install, pytest
  - docker-build : docker build + SHA 기반 이미지 태그

config (ci_setup.json):
  PROJECT_PATH  — 프로젝트 루트 (필수)
  WORKFLOW_TYPE — 'node-test' | 'python-test' | 'docker-build' (필수)
  BRANCH        — 트리거 브랜치 (기본 'main')
"""
import os, sys, json


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "ci_setup.json")


def _log(msg, kind="info"):
    prefix = {"info": "⚙️ ", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def _workflow_node_test(branch):
    return f"""name: Node CI

on:
  push:
    branches: [ "{branch}" ]
  pull_request:
    branches: [ "{branch}" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Node.js 20 설정
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: 의존성 설치
        run: npm ci

      - name: 테스트 실행
        run: npm test
"""


def _workflow_python_test(branch):
    return f"""name: Python CI

on:
  push:
    branches: [ "{branch}" ]
  pull_request:
    branches: [ "{branch}" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python 3.12 설정
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: 의존성 설치
        run: pip install -r requirements.txt

      - name: pytest 실행
        run: pytest
"""


def _workflow_docker_build(branch):
    return f"""name: Docker Build

on:
  push:
    branches: [ "{branch}" ]
  pull_request:
    branches: [ "{branch}" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Docker 이미지 빌드
        run: |
          IMAGE_TAG="${{{{ github.sha }}}}"
          docker build -t myapp:"$IMAGE_TAG" .
          echo "빌드 완료: myapp:$IMAGE_TAG"

      - name: 이미지 확인
        run: docker images myapp
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

    workflow_type = (cfg.get("WORKFLOW_TYPE") or "").strip().lower()
    if workflow_type not in ("node-test", "python-test", "docker-build"):
        _log("WORKFLOW_TYPE 은 'node-test' | 'python-test' | 'docker-build' 중 하나여야 함", "err")
        sys.exit(1)

    branch = (cfg.get("BRANCH") or "main").strip()

    _log(f"타입: {workflow_type} | 브랜치: {branch}", "info")

    if workflow_type == "node-test":
        workflow = _workflow_node_test(branch)
    elif workflow_type == "python-test":
        workflow = _workflow_python_test(branch)
    else:
        workflow = _workflow_docker_build(branch)

    out_path = os.path.join(project, ".github", "workflows", "ci.yml")
    _write(out_path, workflow)
    _log(f"워크플로 생성: {out_path}", "ok")

    print()
    print(f"# ⚙️ CI 워크플로 생성 완료 — {workflow_type}")
    print()
    print(f"| 항목 | 값 |")
    print(f"|------|----|")
    print(f"| WORKFLOW_TYPE | `{workflow_type}` |")
    print(f"| BRANCH | `{branch}` |")
    print(f"| 파일 | `{out_path}` |")
    print()
    print("> 다음 단계: `.github/workflows/ci.yml` 을 커밋 후 push 하면 CI 자동 실행")


if __name__ == "__main__":
    main()
