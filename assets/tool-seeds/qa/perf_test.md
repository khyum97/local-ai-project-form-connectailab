<!-- version: perf_test_v1 -->
# 🧪 perf_test — 성능 테스트 설정 파일 생성

유나가 성능 검증 시 호출 → k6 또는 Artillery 성능 테스트 스크립트 뼈대 생성.

## 동작
1. `TOOL` 에 따라:
   - `k6` → `tests/perf/k6_smoke.js` 생성 (smoke·load·stress 3단계)
   - `artillery` → `tests/perf/artillery.yml` 생성
2. `TARGET_URL`·`VIRTUAL_USERS`·`DURATION` 설정 반영

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `TOOL`: `k6` | `artillery` (기본 `k6`)
- `TARGET_URL`: 테스트 대상 URL (기본 `http://localhost:3000`)
- `VIRTUAL_USERS`: 가상 사용자 수 (기본 10)
- `DURATION`: 테스트 지속 시간 (기본 `30s`)

## 한계
- k6·Artillery 별도 설치 필요
- 인증 토큰 주입 없음 — 수동 추가 필요
