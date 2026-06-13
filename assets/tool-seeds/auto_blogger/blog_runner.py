#!/usr/bin/env python3
# version: blog_runner_v1
"""Diagnose and test the Auto Blogger program."""
import os
import sys
import json
import subprocess

TARGET_DIR = r"E:\CLAUDE-CODE\자동블로그 작성"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog_runner.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def main():
    config = load_config()
    run_mode = config.get("RUN_MODE", "diagnose")

    print("# 자동블로그 작성 프로그램 진단 보고서\n")

    if not os.path.exists(TARGET_DIR):
        print(f"❌ 오류: 대상 디렉토리({TARGET_DIR})가 존재하지 않습니다.")
        sys.exit(1)

    print(f"- **대상 경로:** `{TARGET_DIR}`")
    print(f"- **실행 모드:** `{run_mode}`")

    # 1. 환경변수 파일(.env) 확인
    env_path = os.path.join(TARGET_DIR, ".env")
    if os.path.exists(env_path):
        print("✅ `.env` 설정 파일이 발견되었습니다.")
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            keys = [line.split("=")[0].strip() for line in lines if "=" in line and not line.strip().startswith("#")]
            print(f"  - 정의된 환경변수: {', '.join([f'`{k}`' for k in keys if k])}")
        except Exception as e:
            print(f"  - `.env` 읽기 오류: {e}")
    else:
        print("⚠️ `.env` 설정 파일이 누락되었습니다.")

    # 2. Node.js 환경 점검
    print("\n## Node.js & Playwright 상태")
    try:
        res = subprocess.run(["node", "-v"], capture_output=True, text=True, timeout=5)
        print(f"- **Node.js 버전:** `{res.stdout.strip() or res.stderr.strip()}`")
    except Exception as e:
        print(f"- ⚠️ Node.js 호출 실패: {e}")

    node_modules = os.path.join(TARGET_DIR, "node_modules")
    if os.path.exists(node_modules) and os.path.isdir(node_modules):
        print("- ✅ `node_modules` 디렉토리가 발견되었습니다.")
    else:
        print("- ⚠️ `node_modules`가 존재하지 않습니다. `npm install` 실행이 필요할 수 있습니다.")

    # 3. 테스트 실행 또는 가벼운 진단
    if run_mode == "test":
        print("\n## npm test 실행 결과")
        try:
            res = subprocess.run(["npm", "test"], cwd=TARGET_DIR, capture_output=True, text=True, timeout=30)
            print("```")
            print(res.stdout or res.stderr)
            print("```")
            if res.returncode == 0:
                print("✅ 모든 테스트가 정상 통과했습니다.")
            else:
                print(f"❌ 테스트 실패 (Exit code: {res.returncode})")
        except Exception as e:
            print(f"❌ 테스트 실행 중 오류 발생: {e}")
    else:
        package_json_path = os.path.join(TARGET_DIR, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                print(f"- **정의된 scripts:** {', '.join([f'`{k}`' for k in scripts.keys()])}")
            except Exception as e:
                print(f"- `package.json` 파싱 실패: {e}")

if __name__ == "__main__":
    main()
