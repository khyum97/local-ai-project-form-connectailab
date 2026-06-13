#!/usr/bin/env python3
# version: stock_runner_v1
"""Diagnose and test the Stock Analysis Automation program."""
import os
import sys
import json
import subprocess

TARGET_DIR = r"E:\CLAUDE-CODE\주식 분석 자동화"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_runner.json")

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

    print("# 주식 분석 자동화 프로그램 진단 보고서\n")

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
        print("⚠️ `.env` 설정 파일이 누락되었습니다. `.env.example`을 복사하여 설정하세요.")

    # 2. 최근 로그 파일 확인
    log_dir = os.path.join(TARGET_DIR, "logs")
    if os.path.exists(log_dir) and os.path.isdir(log_dir):
        print("\n## 최근 로그 상태")
        files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            for f in files[:3]:
                size = os.path.getsize(f)
                mtime = os.path.getmtime(f)
                import datetime
                dt = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"- `{os.path.basename(f)}` ({size} bytes, 수정일시: {dt})")
        else:
            print("- 로그 폴더가 비어 있습니다.")
    else:
        print("\n⚠️ 로그 폴더(`logs/`)가 존재하지 않습니다.")

    # 3. 테스트 실행 또는 가벼운 진단
    if run_mode == "test":
        print("\n## pytest 실행 결과")
        try:
            venv_pytest = os.path.join(TARGET_DIR, "venv", "Scripts", "pytest.exe")
            if os.path.exists(venv_pytest):
                cmd = [venv_pytest]
            else:
                cmd = ["pytest"]
            res = subprocess.run(cmd, cwd=TARGET_DIR, capture_output=True, text=True, timeout=30)
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
        print("\n## 기본 시스템 무결성 진단")
        venv_python = os.path.join(TARGET_DIR, "venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            print(f"- 가상환경 파이썬이 설치되어 있습니다: `{venv_python}`")
            try:
                res = subprocess.run([venv_python, "--version"], capture_output=True, text=True)
                print(f"  - 버전: {res.stdout.strip() or res.stderr.strip()}")
            except Exception:
                pass
        else:
            print("- ⚠️ 가상환경(`venv/`)이 감지되지 않았습니다. `setup.bat`을 실행해 가상환경을 구축하세요.")

if __name__ == "__main__":
    main()
