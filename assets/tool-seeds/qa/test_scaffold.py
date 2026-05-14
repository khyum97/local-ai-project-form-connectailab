#!/usr/bin/env python3
# version: test_scaffold_v1
"""테스트 파일 자동 생성 — 프레임워크별 뼈대 + 3개 기본 케이스.

유나가 소스 파일 확인 직후 호출하면:
  1. TARGET_FILE 에서 기본 파일명 추출
  2. TEST_FRAMEWORK 에 따라 경로·형식 결정
  3. happy path / edge case / error case 포함한 뼈대 생성

config:
  PROJECT_PATH   — 프로젝트 루트 경로
  TEST_FRAMEWORK — 'jest' | 'pytest' | 'playwright' (기본 jest)
  TARGET_FILE    — 테스트 대상 소스 파일 (예: src/utils/format.ts)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "test_scaffold.json")
WEB_INIT_CFG = os.path.join(HERE, "web_init.json")


def _log(msg, kind="info"):
    prefix = {"info": "🧪", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _jest_template(name, rel_path):
    return f"""import {{ {name} }} from '{rel_path}';

describe('{name}', () => {{
  it('happy path — 정상 입력 처리', () => {{
    // TODO: 정상 케이스 작성
    expect(true).toBe(true);
  }});

  it('edge case — 경계값 처리', () => {{
    // TODO: 경계값 케이스 작성
    expect(true).toBe(true);
  }});

  it('error case — 잘못된 입력 처리', () => {{
    // TODO: 오류 케이스 작성
    expect(() => {{
      throw new Error('not implemented');
    }}).toThrow();
  }});
}});
"""


def _pytest_template(name):
    return f"""import pytest
# from ... import {name}  # TODO: 실제 임포트 경로 수정


def test_{name}_happy_path():
    \"\"\"happy path — 정상 입력 처리.\"\"\"
    # TODO: 정상 케이스 작성
    assert True


def test_{name}_edge_case():
    \"\"\"edge case — 경계값 처리.\"\"\"
    # TODO: 경계값 케이스 작성
    assert True


def test_{name}_error_case():
    \"\"\"error case — 잘못된 입력 시 예외 발생.\"\"\"
    # TODO: 오류 케이스 작성
    with pytest.raises(Exception):
        raise NotImplementedError
"""


def _playwright_template(name):
    return f"""import {{ test, expect }} from '@playwright/test';

test.describe('{name}', () => {{
  test('happy path — 정상 플로우', async ({{ page }}) => {{
    // TODO: 정상 플로우 작성
    await page.goto('/');
    await expect(page).toHaveTitle(/.*/);
  }});

  test('edge case — 경계 시나리오', async ({{ page }}) => {{
    // TODO: 경계 시나리오 작성
    await page.goto('/');
    expect(true).toBe(true);
  }});

  test('error case — 오류 상태 처리', async ({{ page }}) => {{
    // TODO: 오류 상태 작성
    await page.goto('/404');
    await expect(page.locator('body')).toBeVisible();
  }});
}});
"""


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

    target = (cfg.get("TARGET_FILE") or "").strip()
    if not target:
        _log("TARGET_FILE 이 설정되지 않음", "err")
        sys.exit(1)

    framework = (cfg.get("TEST_FRAMEWORK") or "jest").strip().lower()
    if framework not in ("jest", "pytest", "playwright"):
        _log(f"지원하지 않는 프레임워크: {framework} (jest|pytest|playwright)", "err")
        sys.exit(1)

    base = os.path.splitext(os.path.basename(target))[0]
    _log(f"대상: {target} → 이름: {base}, 프레임워크: {framework}", "info")

    if framework == "jest":
        out_rel = os.path.join("__tests__", f"{base}.test.ts")
        content = _jest_template(base, f"../{target}")
    elif framework == "pytest":
        out_rel = os.path.join("tests", f"test_{base}.py")
        content = _pytest_template(base)
    else:
        out_rel = os.path.join("e2e", f"{base}.spec.ts")
        content = _playwright_template(base)

    out_abs = os.path.join(project, out_rel)

    if os.path.exists(out_abs):
        _log(f"파일 이미 존재 — 덮어쓰지 않음: {out_abs}", "warn")
        sys.exit(1)

    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    _log(f"생성 중: {out_abs}", "step")
    with open(out_abs, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"# ✅ 테스트 파일 생성 완료")
    print()
    print(f"**프레임워크**: {framework}")
    print(f"**파일 경로**: `{out_abs}`")
    print()
    print("포함된 케이스:")
    print("- happy path — 정상 입력 처리")
    print("- edge case — 경계값 처리")
    print("- error case — 오류 케이스")
    print()
    print("> TODO 주석 위치에 실제 단언(assertion)을 작성하세요.")


if __name__ == "__main__":
    main()
