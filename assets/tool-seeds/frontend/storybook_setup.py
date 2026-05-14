#!/usr/bin/env python3
# version: storybook_setup_v1
"""Storybook 초기 설정 자동화 — npx storybook@latest init 실행 + 결과 리포트.

지아가 새 프로젝트에 Storybook 세팅할 때 호출:
  1. PROJECT_PATH 폴더에서 npx storybook@latest init --yes 실행
  2. package.json 존재 여부 사전 확인
  3. 설치 결과 마크다운 리포트 출력

config (storybook_setup.json):
  PROJECT_PATH — Storybook 설치할 프로젝트 루트 폴더
  TIMEOUT      — 명령 타임아웃(초). 기본 300
"""
import os, sys, json, subprocess


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "storybook_setup.json")


def _log(msg, kind="info"):
    prefix = {"info": "📖", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _run(cmd, cwd, timeout=300):
    _log(f"$ {cmd}", "step")
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        combined = (r.stdout or "") + "\n" + (r.stderr or "")
        return r.returncode, combined
    except subprocess.TimeoutExpired:
        return -1, f"⏱ Timeout ({timeout}s) — 타임아웃 초과"
    except Exception as e:
        return -2, str(e)


def main():
    cfg = _load(CONFIG)
    project = (cfg.get("PROJECT_PATH") or "").strip()
    if not project:
        _log("PROJECT_PATH 가 비어 있습니다.", "err")
        sys.exit(1)

    project = os.path.expanduser(project)
    if not os.path.isdir(project):
        _log(f"폴더 없음: {project}", "err")
        sys.exit(1)

    # package.json 존재 확인
    pkg_path = os.path.join(project, "package.json")
    if not os.path.exists(pkg_path):
        _log("package.json 없음 — Node 프로젝트 루트인지 확인하세요.", "err")
        sys.exit(1)

    timeout = int(cfg.get("TIMEOUT", 300))
    _log(f"Storybook 설치 대상: {project}", "info")
    _log(f"타임아웃: {timeout}초", "info")

    # storybook init 실행
    cmd = "npx storybook@latest init --yes"
    code, output = _run(cmd, cwd=project, timeout=timeout)

    # 결과 리포트
    print()
    print(f"# 📖 storybook_setup 결과 — {os.path.basename(project)}")
    print()
    print(f"- **대상 경로**: `{project}`")
    print(f"- **실행 명령**: `{cmd}`")
    print(f"- **종료 코드**: `{code}`")
    print()

    if code == 0:
        _log("Storybook 설치 완료", "ok")
        print("## ✅ 설치 성공")
        print()
        print("Storybook이 정상적으로 설치되었습니다.")
        print()
        print("### 다음 단계")
        print()
        print("```bash")
        print("npm run storybook   # 개발 서버 시작 (기본 포트 6006)")
        print("npm run build-storybook   # 정적 빌드")
        print("```")
    else:
        _log(f"설치 실패 (exit code {code})", "err")
        print("## ❌ 설치 실패")
        print()
        print(f"종료 코드: `{code}`")
        print()
        print("### 마지막 로그 (최대 30줄)")
        print()
        print("```")
        for line in output.strip().split("\n")[-30:]:
            print(line)
        print("```")
        print()
        print("> ⚠️ 위 로그를 확인하여 원인을 파악하세요.")
        print("> 네트워크 문제라면 TIMEOUT 값을 늘리거나 재시도하세요.")
        sys.exit(1)

    # 성공 시에도 전체 로그 접을 수 있게 포함
    print()
    print("<details>")
    print("<summary>전체 설치 로그 보기</summary>")
    print()
    print("```")
    print(output.strip()[:3000])  # 너무 길면 앞 3000자만
    print("```")
    print("</details>")


if __name__ == "__main__":
    main()
