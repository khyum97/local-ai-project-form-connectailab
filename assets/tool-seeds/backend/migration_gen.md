<!-- version: migration_gen_v1 -->
# ⚙️ migration_gen — DB 마이그레이션 파일 생성

민준이 새 테이블/컬럼 설계 시 호출 → SQL 또는 Prisma 마이그레이션 뼈대 자동 생성.

## 동작
1. `MIGRATION_TYPE` 에 따라:
   - `sql` → `migrations/YYYYMMDD_HHMMSS_{NAME}.sql` (CREATE TABLE + rollback)
   - `prisma` → `prisma/migrations/{timestamp}_{name}/migration.sql` 구조
2. 타임스탬프 포함 파일명으로 충돌 방지

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `MIGRATION_NAME`: 마이그레이션 이름 (예: `create_users_table`)
- `MIGRATION_TYPE`: `sql` | `prisma` (기본 `sql`)
- `TABLE_NAME`: 주 테이블 이름 (기본 `table_name`)

## 한계
- 컬럼 자동 추론 없음 — TODO 로 표시, 직접 작성 필요
- Prisma schema.prisma 자동 수정 없음
