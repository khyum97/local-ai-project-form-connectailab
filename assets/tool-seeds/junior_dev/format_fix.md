<!-- version: format_fix_v1 -->
# ✨ format_fix — 코드 포맷 자동 수정

연아가 코드 작성·수정 후 호출 → 지정 포매터 실행 → 수정된 파일 목록 + 오류 요약 리포트.

## 동작
1. `FORMATTER` 에 따라 명령 실행:
   - `prettier` → `npx prettier --write . --ignore-path .gitignore` (node_modules 자동 제외)
   - `eslint` → `npx eslint --fix src/`
   - `black` → `black .`
   - `ruff` → `ruff check --fix .`
2. 표준 출력·표준 오류에서 수정된 파일 목록 파싱
3. 종료 코드 + 수정 파일 수 + 오류 요약 리포트

## 설정
- `PROJECT_PATH`: 포맷 적용할 프로젝트 루트
- `FORMATTER`: `prettier` | `eslint` | `black` | `ruff` (기본 `prettier`)

## 한계
- 포맷터 미설치 시 실패 — `npx`, `black`, `ruff` 사전 설치 필요
- `eslint --fix` 는 `src/` 만 대상 — 다른 경로는 수동 조정 필요
- 포맷 오류(파싱 실패 등)는 자동 수정 불가, 리포트만 제공
