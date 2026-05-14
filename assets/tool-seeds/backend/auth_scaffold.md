<!-- version: auth_scaffold_v1 -->
# ⚙️ auth_scaffold — JWT 인증 뼈대 생성

민준이 인증 기능 구현 시 호출 → JWT 미들웨어·라우트·유저 모델 뼈대 파일 자동 생성.

## 동작
1. `FRAMEWORK` 에 따라 뼈대 생성:
   - `express` → `src/middleware/auth.ts`, `src/routes/auth.ts`
   - `fastapi` → `app/auth/jwt.py`, `app/auth/router.py`
2. 파일 생성 후 경로 출력

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `FRAMEWORK`: `express` | `fastapi` (기본 `express`)
- `SECRET_ENV`: JWT secret 환경변수명 (기본 `JWT_SECRET`)

## 한계
- refresh token 구현 없음 — access token 단순 구조만
- DB 연동 코드 없음 — TODO 로 표시
