#!/usr/bin/env python3
# version: deploy_check_v1
"""배포 상태 확인 도구 — urllib.request 기반, 외부 의존성 없음.

서준이 배포 후 TARGET_URL에 HTTP GET 요청을 보내 결과를 확인한다:
  - 상태 코드 vs EXPECTED_STATUS 비교
  - 응답 시간(ms) 측정
  - 주요 응답 헤더 요약

config (deploy_check.json):
  TARGET_URL      — 확인할 URL (필수)
  EXPECTED_STATUS — 기대 상태 코드 (기본 200)
  TIMEOUT_SECONDS — 타임아웃 초 (기본 10)
"""
import os, sys, json, time
import urllib.request
import urllib.error


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "deploy_check.json")

SUMMARY_HEADERS = [
    "content-type",
    "content-length",
    "server",
    "x-powered-by",
    "cache-control",
    "last-modified",
    "etag",
]


def _log(msg, kind="info"):
    prefix = {"info": "🔍", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    cfg = _load(CONFIG)

    target_url = (cfg.get("TARGET_URL") or "").strip()
    if not target_url:
        _log("TARGET_URL 설정 필요", "err")
        sys.exit(1)

    expected_status = int(cfg.get("EXPECTED_STATUS") or 200)
    timeout = int(cfg.get("TIMEOUT_SECONDS") or 10)

    _log(f"대상: {target_url}", "info")
    _log(f"기대 상태: {expected_status} | 타임아웃: {timeout}s", "info")

    req = urllib.request.Request(
        target_url,
        headers={"User-Agent": "deploy-check/1.0"},
        method="GET",
    )

    start = time.monotonic()
    actual_status = None
    headers_dict = {}
    error_msg = None

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            actual_status = resp.status
            headers_dict = {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        actual_status = e.code
        headers_dict = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        error_msg = str(e.reason)
    except urllib.error.URLError as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        error_msg = str(e.reason)
    except Exception as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        error_msg = str(e)

    # 성공 여부 판정
    if actual_status is not None:
        success = (actual_status == expected_status)
    else:
        success = False

    # 결과 출력
    print()
    icon = "✅" if success else "❌"
    print(f"# {icon} 배포 상태 확인 — {target_url}")
    print()
    print(f"| 항목 | 값 |")
    print(f"|------|----|")
    print(f"| URL | `{target_url}` |")
    print(f"| 기대 상태 | `{expected_status}` |")
    print(f"| 실제 상태 | `{actual_status if actual_status is not None else 'N/A'}` |")
    print(f"| 응답 시간 | `{elapsed_ms}ms` |")
    print(f"| 결과 | {'**성공**' if success else '**실패**'} |")

    if error_msg:
        print(f"| 오류 | `{error_msg}` |")

    if headers_dict:
        print()
        print("## 응답 헤더 요약")
        print()
        found_any = False
        for h in SUMMARY_HEADERS:
            if h in headers_dict:
                print(f"- **{h}**: `{headers_dict[h]}`")
                found_any = True
        if not found_any:
            print("- (주요 헤더 없음)")

    print()
    if success:
        print(f"> 배포 정상 확인. 응답 {elapsed_ms}ms 이내 수신.")
    elif actual_status is not None:
        print(f"> 상태 코드 불일치. 예상 {expected_status}, 실제 {actual_status}.")
    else:
        print(f"> 요청 실패 — 네트워크 또는 URL 확인 필요.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
