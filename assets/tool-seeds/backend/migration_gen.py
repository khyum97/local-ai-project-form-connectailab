#!/usr/bin/env python3
# version: migration_gen_v1
"""DB 마이그레이션 파일 생성 — SQL 또는 Prisma 뼈대.

config:
  PROJECT_PATH    — 프로젝트 루트
  MIGRATION_NAME  — 마이그레이션 이름
  MIGRATION_TYPE  — 'sql' | 'prisma' (기본 sql)
  TABLE_NAME      — 주 테이블명 (기본 table_name)
"""
import os, sys, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "migration_gen.json")

SQL_TEMPLATE = """-- Migration: {name}
-- Created: {ts}

-- ▲ UP
CREATE TABLE IF NOT EXISTS {table} (
    id          BIGSERIAL PRIMARY KEY,
    -- TODO: 컬럼 정의 추가
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- TODO: 인덱스 추가
-- CREATE INDEX idx_{table}_created_at ON {table}(created_at);

-- ▼ DOWN (rollback)
-- DROP TABLE IF EXISTS {table};
"""

PRISMA_TEMPLATE = """-- Migration: {name}
-- Created: {ts}

CREATE TABLE "{table}" (
    "id"         BIGSERIAL PRIMARY KEY,
    -- TODO: 컬럼 정의 추가
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

def _log(msg, kind="info"):
    prefix = {"info": "⚙️", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
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
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    mig_name = (cfg.get("MIGRATION_NAME") or "migration").strip().lower().replace(" ", "_")
    mig_type = (cfg.get("MIGRATION_TYPE") or "sql").strip().lower()
    table = (cfg.get("TABLE_NAME") or "table_name").strip().lower()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if mig_type == "sql":
        out_dir = os.path.join(project, "migrations")
        filename = f"{ts}_{mig_name}.sql"
        content = SQL_TEMPLATE.format(name=mig_name, ts=ts_human, table=table)
    elif mig_type == "prisma":
        out_dir = os.path.join(project, "prisma", "migrations", f"{ts}_{mig_name}")
        filename = "migration.sql"
        content = PRISMA_TEMPLATE.format(name=mig_name, ts=ts_human, table=table)
    else:
        _log(f"지원하지 않는 타입: {mig_type}", "err")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    _log(f"생성: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print("# ✅ 마이그레이션 파일 생성 완료")
    print(f"\n**이름**: {mig_name} | **타입**: {mig_type} | **테이블**: {table}")
    print(f"**파일**: `{os.path.relpath(out_path, project)}`")
    print("\n> TODO 주석에 컬럼 정의를 추가하세요.")

if __name__ == "__main__":
    main()
