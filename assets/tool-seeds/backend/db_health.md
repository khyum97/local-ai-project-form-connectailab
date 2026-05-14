<!-- version: db_health_v1 -->
# 🩺 db_health — 데이터베이스 연결 상태 확인

민준이 배포 전 또는 장애 트리아지 시 호출 → DB 연결 성공/실패 + 응답 시간 리포트.

## 동작
1. `DB_TYPE` 감지 — `sqlite`, `postgresql`, `mysql`
2. DB 유형별 연결 시도:
   - `sqlite`: 파일 존재 확인 + `SELECT 1` 실행
   - `postgresql`: `psycopg2` import 시도 → 연결 → `SELECT 1`
   - `mysql`: `pymysql` import 시도 → 연결 → `SELECT 1`
3. 드라이버 미설치 시 import 실패 메시지 리포트 (크래시 없음)
4. 연결 성공/실패 + 응답 시간(ms) 출력

## 설정
- `DB_TYPE`: `'postgresql'` | `'mysql'` | `'sqlite'` (필수)
- `DB_URL`: 연결 문자열 (필수)
  - sqlite: 파일 경로 (예: `'/app/data/db.sqlite3'`)
  - postgresql: `postgresql://user:pass@host:port/dbname`
  - mysql: `mysql://user:pass@host:port/dbname`

## 한계
- `psycopg2`, `pymysql` 미설치 시 연결 불가 — pip 설치 안내만 제공
- 연결 타임아웃 기본 5초 고정
- SSL/TLS 옵션 미지원
