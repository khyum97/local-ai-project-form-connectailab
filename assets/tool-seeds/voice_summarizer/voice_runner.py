#!/usr/bin/env python3
# version: voice_runner_v1
"""Diagnose and test the Voice Summarization program."""
import os
import sys
import json
import subprocess

TARGET_DIR = r"E:\CLAUDE-CODE\음성녹음 요약"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_runner.json")

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

    print("# 음성녹음 요약 프로그램 진단 보고서\n")

    if not os.path.exists(TARGET_DIR):
        print(f"❌ 오류: 대상 디렉토리({TARGET_DIR})가 존재하지 않습니다.")
        sys.exit(1)

    print(f"- **대상 경로:** `{TARGET_DIR}`")
    print(f"- **실행 모드:** `{run_mode}`")

    # 1. 라이선스 및 일련번호 키 검토
    serial_path = os.path.join(TARGET_DIR, "ADMIN_SERIAL_KEY.txt")
    license_path = os.path.join(TARGET_DIR, "license.json")
    if os.path.exists(serial_path):
        with open(serial_path, "r", encoding="utf-8") as f:
            key = f.read().strip()
        print(f"✅ `ADMIN_SERIAL_KEY.txt`가 확인되었습니다.")
    else:
        print("⚠️ `ADMIN_SERIAL_KEY.txt`가 존재하지 않습니다.")

    if os.path.exists(license_path):
        print("✅ `license.json` 라이선스 매니페스트가 확인되었습니다.")
        try:
            with open(license_path, "r", encoding="utf-8") as f:
                lic = json.load(f)
            print(f"  - 라이선스 정보: {lic.get('type', 'Unknown')} (만료일: {lic.get('expires', 'N/A')})")
        except Exception as e:
            print(f"  - 라이선스 파일 파싱 실패: {e}")

    # 2. 음성 데이터 및 요약 데이터 디렉토리 감사
    records_dir = os.path.join(TARGET_DIR, "records")
    if os.path.exists(records_dir) and os.path.isdir(records_dir):
        print("\n## 수집 데이터 상태")
        files = [os.path.join(records_dir, f) for f in os.listdir(records_dir) if os.path.isfile(os.path.join(records_dir, f))]
        print(f"- **총 녹음/변환 파일 개수:** `{len(files)}`개")
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            for f in files[:3]:
                size = os.path.getsize(f)
                print(f"  - `{os.path.basename(f)}` ({size} bytes)")
    else:
        print("\n⚠️ 녹음 데이터 디렉토리(`records/`)가 존재하지 않습니다.")

    # 3. 가상환경 및 Whisper 라이브러리 검사
    print("\n## 종속성 및 가상환경 상태")
    venv_python = os.path.join(TARGET_DIR, "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        print(f"- 가상환경 파이썬: `{venv_python}`")
        try:
            check_script = "import sys; print('python:', sys.version.split()[0]);"
            check_script += "try: import whisper; print('whisper: OK')\nexcept: print('whisper: Missing')\n"
            check_script += "try: import torch; print('torch:', torch.__version__)\nexcept: print('torch: Missing')"
            res = subprocess.run([venv_python, "-c", check_script], capture_output=True, text=True, timeout=10)
            for line in res.stdout.splitlines():
                print(f"  - {line}")
        except Exception as e:
            print(f"  - 종속성 체크 실패: {e}")
    else:
        print("- ⚠️ 가상환경(`venv/`)을 찾을 수 없습니다. `install.bat`을 실행해 라이브러리를 설치하세요.")

if __name__ == "__main__":
    main()
