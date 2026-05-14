#!/usr/bin/env python3
# version: db_health_v1
"""데이터베이스 연결 상태 확인 도구.

민준이 배포 전 또는 장애 트리아지 시 이 도구를 호출하면:
  1. DB_TYPE (sqlite|postgresql|mysql) 확인
  2. DB_URL 기반 연결 시도
  3. SELECT 1 실행 후 응답 시간 측정
  4. 연결 성공/실패 + ms 단위 응답 시간 리포트

config:
  DB_TYPE — 'sqlite' | 'postgresql' | 'mysql' (필수)
  DB_URL  — 연결 문자열 또는 파일 경로 (필수)
"""
import os, sys, json, time, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "db_health.json")

ALLOWED_DB_TYPES = ("sqlite", "postgresql", "mysql")
CONNECT_TIMEOUT = 5


def _log(msg, kind="info"):
    prefix = {"info": "🩺", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _parse_db_url(url):
    """mysql://user:pass@host:port/dbname 또는 postgresql:// 파싱."""
    pattern = r"^(?:postgresql|mysql|postgres)://([^:]*):([^@]*)@([^:/]+):?(\d*)/(.+)$"
    m = re.match(pattern, url)
    if not m:
        return None
    return {
        "user": m.group(1),
        "password": m.group(2),
        "host": m.group(3),
        "port": int(m.group(4)) if m.group(4) else None,
        "database": m.group(5),
    }


def _check_sqlite(db_url):
    path = db_url.replace("sqlite:///", "").replace("sqlite://", "")
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return False, f"파일 없음: {path}", None
    try:
        import sqlite3
        t0 = time.perf_counter()
        conn = sqlite3.connect(path, timeout=CONNECT_TIMEOUT)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        elapsed = (time.perf_counter() - t0) * 1000
        conn.close()
        if result and result[0] == 1:
            return True, f"SELECT 1 → {result[0]}", elapsed
        return False, "SELECT 1 응답 이상", elapsed
    except Exception as e:
        return False, str(e), None


def _check_postgresql(db_url):
    try:
        import psycopg2
    except ImportError:
        return False, "psycopg2 미설치 — `pip install psycopg2-binary` 실행 필요", None
    parsed = _parse_db_url(db_url)
    if not parsed:
        return False, f"DB_URL 파싱 실패: {db_url}", None
    try:
        t0 = time.perf_counter()
        conn = psycopg2.connect(
            host=parsed["host"],
            port=parsed["port"] or 5432,
            user=parsed["user"],
            password=parsed["password"],
            dbname=parsed["database"],
            connect_timeout=CONNECT_TIMEOUT,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        elapsed = (time.perf_counter() - t0) * 1000
        conn.close()
        if result and result[0] == 1:
            return True, f"SELECT 1 → {result[0]}", elapsed
        return False, "SELECT 1 응답 이상", elapsed
    except Exception as e:
        return False, str(e), None


def _check_mysql(db_url):
    try:
        import pymysql
    except ImportError:
        return False, "pymysql 미설치 — `pip install pymysql` 실행 필요", None
    parsed = _parse_db_url(db_url)
    if not parsed:
        return False, f"DB_URL 파싱 실패: {db_url}", None
    try:
        t0 = time.perf_counter()
        conn = pymysql.connect(
            host=parsed["host"],
            port=parsed["port"] or 3306,
            user=parsed["user"],
            password=parsed["password"],
            database=parsed["database"],
            connect_timeout=CONNECT_TIMEOUT,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        elapsed = (time.perf_counter() - t0) * 1000
        conn.close()
        if result and result[0] == 1:
            return True, f"SELECT 1 → {result[0]}", elapsed
        return False, "SELECT 1 응답 이상", elapsed
    except Exception as e:
        return False, str(e), None


def main():
    cfg = _load(CONFIG)

    db_type = (cfg.get("DB_TYPE") or "").strip().lower()
    db_url = (cfg.get("DB_URL") or "").strip()

    if db_type not in ALLOWED_DB_TYPES:
        _log(f"DB_TYPE 오류: '{db_type}'. 허용: {ALLOWED_DB_TYPES}", "err")
        sys.exit(1)
    if not db_url:
        _log("DB_URL 비어있음", "err")
        sys.exit(1)

    _log(f"DB 유형: {db_type}", "info")
    _log(f"연결 시도 중...", "step")

    if db_type == "sqlite":
        success, message, elapsed_ms = _check_sqlite(db_url)
    elif db_type == "postgresql":
        success, message, elapsed_ms = _check_postgresql(db_url)
    else:
        success, message, elapsed_ms = _check_mysql(db_url)

    print()
    print(f"# 🩺 db_health 결과")
    print()
    print(f"**DB 유형**: `{db_type}`")
    print(f"**연결 URL**: `{db_url}`")
    print()

    if success:
        print(f"## ✅ 연결 성공")
        print()
        print(f"- **응답**: {message}")
        if elapsed_ms is not None:
            print(f"- **응답 시간**: `{elapsed_ms:.2f} ms`")
        print()
        print("> ✅ DB 연결 정상. 안전하게 다음 단계로.")
    else:
        print(f"## ❌ 연결 실패")
        print()
        print(f"- **원인**: {message}")
        if elapsed_ms is not None:
            print(f"- **응답 시간**: `{elapsed_ms:.2f} ms` (실패 전)")
        print()
        print("> ⚠️ DB 연결 실패 — 위 원인 확인 후 재시도.")
        sys.exit(1)


if __name__ == "__main__":
    main()
