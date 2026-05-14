#!/usr/bin/env python3
# version: env_check_v1
"""환경변수 검증 도구 — .env.example 대비 누락 키 리포트.

민준이 배포 전 또는 팀원 환경 세팅 시 이 도구를 호출하면:
  1. PROJECT_PATH/.env.example 파싱 → 필수 키 목록 추출
  2. PROJECT_PATH/.env (또는 ENV_FILE 지정) 파싱
  3. .env 없으면 os.environ 대신 사용
  4. 누락 키 마크다운 리포트

config:
  PROJECT_PATH — 검사할 프로젝트 경로 (필수)
  ENV_FILE     — 비교할 env 파일명 (기본 '.env')
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "env_check.json")


def _log(msg, kind="info"):
    prefix = {"info": "🔐", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _parse_env_file(path):
    """dotenv 없이 KEY=VALUE 형식 파싱. 주석·빈 줄 제외. 값은 무시, 키만 반환."""
    keys = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key:
                        keys[key] = val
    except Exception as e:
        _log(f"파일 파싱 실패: {path} — {e}", "warn")
    return keys


def _parse_example_keys(path):
    """KEY=VALUE 또는 KEY= 또는 # KEY 형식에서 키만 추출."""
    keys = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                if "=" in line:
                    key = line.partition("=")[0].strip()
                    if key:
                        keys.append(key)
    except Exception as e:
        _log(f".env.example 파싱 실패: {e}", "err")
    return keys


def main():
    cfg = _load(CONFIG)

    project = (cfg.get("PROJECT_PATH") or "").strip()
    env_file_name = (cfg.get("ENV_FILE") or ".env").strip()

    if not project:
        _log("PROJECT_PATH 비어있음", "err")
        sys.exit(1)
    project = os.path.expanduser(project)
    if not os.path.isdir(project):
        _log(f"폴더 없음: {project}", "err")
        sys.exit(1)

    example_path = os.path.join(project, ".env.example")
    if not os.path.exists(example_path):
        _log(f".env.example 없음: {example_path}", "err")
        sys.exit(1)

    _log(f"프로젝트: {project}", "info")
    _log(f"파싱 중: .env.example", "step")
    required_keys = _parse_example_keys(example_path)
    _log(f"필수 키 {len(required_keys)}개 감지", "info")

    env_path = os.path.join(project, env_file_name)
    using_system_env = False
    if os.path.exists(env_path):
        _log(f"파싱 중: {env_file_name}", "step")
        current_env = _parse_env_file(env_path)
        source_label = env_file_name
    else:
        _log(f"{env_file_name} 없음 → os.environ 사용", "warn")
        current_env = dict(os.environ)
        source_label = "os.environ"
        using_system_env = True

    missing = [k for k in required_keys if k not in current_env]
    present = [k for k in required_keys if k in current_env]

    print()
    print(f"# 🔐 env_check 결과 — {os.path.basename(project)}")
    print()
    print(f"**비교 대상**: `{source_label}`")
    print(f"**필수 키**: {len(required_keys)}개 | **존재**: {len(present)}개 | **누락**: {len(missing)}개")
    print()

    if missing:
        print("## ❌ 누락된 환경변수")
        print()
        for k in missing:
            print(f"- `{k}`")
        print()
        print("> ⚠️ 누락 키를 `.env` 또는 환경변수에 설정 후 재실행.")
        sys.exit(1)
    else:
        print("## ✅ 모든 필수 환경변수 존재")
        print()
        for k in present:
            print(f"- `{k}`")
        print()
        print("> ✅ 환경변수 검증 통과. 안전하게 다음 단계로.")


if __name__ == "__main__":
    main()
