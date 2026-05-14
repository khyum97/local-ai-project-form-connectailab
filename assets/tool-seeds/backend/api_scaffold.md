<!-- version: api_scaffold_v1 -->
# 🛠 api_scaffold — REST API 엔드포인트 보일러플레이트 생성

민준이 코드를 작성할 때 호출 → 프레임워크에 맞는 라우터 파일을 OUTPUT_DIR에 생성.

## 동작
1. `FRAMEWORK` 감지 — `express` 또는 `fastapi`
2. `ENDPOINT`, `METHOD` 기반으로 보일러플레이트 코드 생성
   - `express`: TypeScript 라우터 파일 (`router.ts`) 생성 — request/response 타입 포함
   - `fastapi`: Python 라우터 파일 (`router.py`) 생성 — Pydantic 모델 + 응답 타입 포함
3. `OUTPUT_DIR` 에 파일 저장 후 생성 경로 리포트

## 설정
- `FRAMEWORK`: `'express'` 또는 `'fastapi'` (필수)
- `ENDPOINT`: API 경로 (예: `'/users'`, `'/items/{id}'`) (필수)
- `METHOD`: `'GET'` | `'POST'` | `'PUT'` | `'DELETE'` (기본 `'GET'`)
- `OUTPUT_DIR`: 출력 폴더 경로 (비우면 현재 디렉토리)

## 한계
- 단일 엔드포인트만 처리 — 여러 엔드포인트 생성 시 반복 호출 필요
- DB 연동 코드 미포함 — 순수 라우터/핸들러 보일러플레이트만 생성
- 인증(Auth) 미들웨어 자동 삽입 없음
