#!/usr/bin/env python3
# version: format_fix_v1
"""코드 포맷 자동 수정 — 포매터 실행 + 수정 파일 목록 + 오류 요약.

연아가 코드 작성·수정 후 호출하면:
  1. FORMATTER 에 따라 명령 실행
  2. 수정된 파일 수 + 오류 요약 리포트

config:
  PROJECT_PATH — 포맷 적용할 프로젝트 루트
  FORMATTER    — 'prettier' | 'eslint' | 'black' | 'ruff' (기본 prettier)
"""
import os, sys, json, subprocess, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "format_fix.json")
WEB_INIT_CFG = os.path.join(HERE, "web_init.json")


def _log(msg, kind="info"):
    prefix = {"info": "✨", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _run(cmd, cwd, timeout=180):
    _log(f"$ {cmd}", "step")
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or ""), (r.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout ({timeout}s)"
    except Exception as e:
        return -2, "", str(e)


def _parse_fixed_files(formatter, stdout, stderr):
    """포매터별 수정 파일 목록 파싱."""
    combined = stdout + "\n" + stderr
    files = []
    if formatter == "prettier":
        # prettier: 수정된 파일은 한 줄씩 출력
        for line in combined.splitlines():
            line = line.strip()
            if line and not line.startswith("(") and "prettier" not in line.lower():
                files.append(line)
    elif formatter == "black":
        # black: "reformatted <path>"
        for line in combined.splitlines():
            m = re.match(r"reformatted (.+)", line.strip())
            if m:
                files.append(m.group(1))
    elif formatter == "ruff":
        # ruff: "Fixed <n> error(s)" 또는 파일명 출력
        for line in combined.splitlines():
            line = line.strip()
            if line.endswith(".py") or line.endswith(".pyi"):
                files.append(line)
    elif formatter == "eslint":
        # eslint --fix 는 수정 파일 명시 없음, 오류만 출력
        pass
    return files


def main():
    cfg = _load(CONFIG)
    init_cfg = _load(WEB_INIT_CFG)

    project = (cfg.get("PROJECT_PATH") or "").strip()
    if not project:
        project = (init_cfg.get("LAST_PROJECT") or "").strip()
    if not project:
        _log("PROJECT_PATH 비어있고 web_init 기록도 없음", "err")
        sys.exit(1)
    project = os.path.expanduser(project)
    if not os.path.isdir(project):
        _log(f"폴더 없음: {project}", "err")
        sys.exit(1)

    formatter = (cfg.get("FORMATTER") or "prettier").strip().lower()
    if formatter not in ("prettier", "eslint", "black", "ruff"):
        _log(f"지원하지 않는 포매터: {formatter} (prettier|eslint|black|ruff)", "err")
        sys.exit(1)

    _log(f"포맷 대상: {project} | 포매터: {formatter}", "info")

    cmd_map = {
        "prettier": "npx prettier --write . --ignore-path .gitignore",
        "eslint":   "npx eslint --fix src/",
        "black":    "black .",
        "ruff":     "ruff check --fix .",
    }
    cmd = cmd_map[formatter]
    code, stdout, stderr = _run(cmd, cwd=project)
    fixed_files = _parse_fixed_files(formatter, stdout, stderr)

    print()
    print(f"# ✨ 포맷 수정 결과 — {formatter}")
    print()
    print(f"**명령**: `{cmd}`")
    print(f"**종료 코드**: {code}")
    print()

    if fixed_files:
        print(f"## ✅ 수정된 파일 ({len(fixed_files)}개)")
        for fp in fixed_files[:50]:
            print(f"- `{fp}`")
        if len(fixed_files) > 50:
            print(f"- ... 외 {len(fixed_files) - 50}개")
        print()
    else:
        if code == 0:
            print("## ✅ 수정 사항 없음 (이미 포맷 완료)")
        else:
            print("## ⚠️ 수정 파일 목록 파싱 불가 — 출력 확인 필요")
        print()

    if stderr.strip():
        print("## 오류/경고 요약 (마지막 15줄)")
        print("```")
        for line in stderr.strip().split("\n")[-15:]:
            print(line)
        print("```")
        print()

    if code != 0:
        print(f"> ❌ 포매터 종료 코드 {code} — 오류 확인 후 수동 수정 필요.")
        sys.exit(1)
    else:
        print("> 포맷 완료.")


if __name__ == "__main__":
    main()
