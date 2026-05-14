<!-- version: util_scaffold_v1 -->
# 🌱 util_scaffold — 유틸 함수 뼈대 생성

연아가 공통 유틸 함수 작성 시 호출 → 카테고리별 뼈대 파일 자동 생성.

## 동작
1. `UTIL_TYPE` 에 따라 뼈대 파일 생성:
   - `date` → `src/utils/date.ts` (날짜 포맷·파싱)
   - `string` → `src/utils/string.ts` (문자열 처리)
   - `number` → `src/utils/number.ts` (숫자 포맷·계산)
   - `http` → `src/utils/http.ts` (fetch 래퍼)
2. 함수 시그니처 + JSDoc + TODO 포함

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `UTIL_TYPE`: `date` | `string` | `number` | `http` (기본 `string`)

## 한계
- TypeScript 전용 — JS 프로젝트는 .ts → .js 수동 변경 필요
