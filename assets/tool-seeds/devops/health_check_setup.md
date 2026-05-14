<!-- version: health_check_setup_v1 -->
# 🚀 health_check_setup — 헬스체크 엔드포인트 설정 파일 생성

서준이 서비스 배포 전 호출 → Express·FastAPI·Nginx 헬스체크 설정 뼈대 생성.

## 동작
1. `FRAMEWORK` 에 따라:
   - `express` → `src/routes/health.ts` 생성
   - `fastapi` → `app/health.py` 생성
   - `nginx` → `nginx/health.conf` 생성
2. `/health` GET 엔드포인트 — DB·버전·uptime 응답

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `FRAMEWORK`: `express` | `fastapi` | `nginx` (기본 `express`)

## 한계
- DB 연결 체크는 TODO — 직접 구현 필요
