#!/usr/bin/env python3
# version: coverage_check_v1
"""커버리지 측정 + 임계값 검사 — 현재 % 추출 후 통과/실패 리포트.

유나가 테스트 생성·수정 후 호출하면:
  1. package.json 의 coverage 스크립트 있으면 npm run coverage
  2. 없으면 jest --coverage 또는 pytest --cov 시도
  3. 출력에서 커버리지 % 추출 후 THRESHOLD 와 비교

config:
  PROJECT_PATH — 검사할 프로젝트 루트
  THRESHOLD    — 최소 커버리지 % (기본 80)
"""
import os, sys, json, subprocess, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "coverage_check.json")
WEB_INIT_CFG = os.path.join(HERE, "web_init.json")


def _log(msg, kind="info"):
    prefix = {"info": "📊", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + "\n" + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, f"Timeout ({timeout}s)"
    except Exception as e:
        return -2, str(e)


def _extract_pct(output):
    """출력에서 커버리지 % 추출. 여러 패턴 시도."""
    # pytest-cov: "TOTAL   100    20    80%"
    m = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+(?:\.\d+)?)%", output)
    if m:
        return float(m.group(1))
    # jest: "All files | 80.5 | ..." 또는 "All files | 80.5%"
    m = re.search(r"All files\s*\|\s*(\d+(?:\.\d+)?)", output)
    if m:
        return float(m.group(1))
    # 일반: "Coverage: 75.3%"
    m = re.search(r"[Cc]overage[:\s]+(\d+(?:\.\d+)?)%", output)
    if m:
        return float(m.group(1))
    # 마지막 % 숫자 (폴백)
    nums = re.findall(r"(\d+(?:\.\d+)?)%", output)
    if nums:
        return float(nums[-1])
    return None


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

    try:
        threshold = float(cfg.get("THRESHOLD", 80))
    except (TypeError, ValueError):
        threshold = 80.0

    _log(f"검사 대상: {project} | 임계값: {threshold}%", "info")

    label, code, output = None, None, None

    # 1) package.json coverage 스크립트
    pkg_path = os.path.join(project, "package.json")
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            if "coverage" in pkg.get("scripts", {}):
                code, output = _run("npm run coverage", cwd=project)
                label = "npm run coverage"
        except Exception:
            pass

    # 2) jest --coverage
    if label is None:
        ts_files = glob.glob(os.path.join(project, "**/*.ts"), recursive=True) + \
                   glob.glob(os.path.join(project, "**/*.tsx"), recursive=True)
        ts_files = [f for f in ts_files if "node_modules" not in f]
        if ts_files:
            code, output = _run("npx jest --coverage --passWithNoTests", cwd=project)
            label = "npx jest --coverage"

    # 3) pytest --cov
    if label is None:
        py_files = glob.glob(os.path.join(project, "**/*.py"), recursive=True)
        py_files = [f for f in py_files if "venv" not in f and ".venv" not in f and "__pycache__" not in f]
        if py_files:
            code, output = _run("pytest --cov --cov-report=term-missing", cwd=project)
            label = "pytest --cov"

    print()
    print(f"# 📊 커버리지 검사 결과")
    print()

    if label is None:
        print("⚠️ 실행할 커버리지 도구 없음 (package.json scripts 없고 .ts/.py 파일도 없음)")
        return

    print(f"**실행**: `{label}`")
    print(f"**종료 코드**: {code}")
    print()

    pct = _extract_pct(output)

    if pct is not None:
        passed = pct >= threshold
        icon = "✅" if passed else "❌"
        print(f"## {icon} 커버리지: **{pct:.1f}%** (임계값: {threshold:.0f}%)")
        print()
        if passed:
            print(f"> 임계값 통과. ({pct:.1f}% >= {threshold:.0f}%)")
        else:
            print(f"> ⚠️ 임계값 미달. ({pct:.1f}% < {threshold:.0f}%) — 테스트 보강 필요.")
    else:
        print("## ⚠️ 커버리지 % 파싱 실패 — 원시 출력 확인 필요")

    print()
    print("### 출력 (마지막 20줄)")
    print("```")
    for line in output.strip().split("\n")[-20:]:
        print(line)
    print("```")

    if pct is not None and pct < threshold:
        sys.exit(1)


if __name__ == "__main__":
    main()
