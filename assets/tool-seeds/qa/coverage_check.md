<!-- version: coverage_check_v1 -->
# 📊 coverage_check — 커버리지 측정 + 임계값 검사

유나가 테스트 생성·수정 후 호출 → 현재 커버리지 % 측정 → 임계값 통과 여부 리포트.

## 동작
1. `package.json` 에 `coverage` 스크립트 있으면 `npm run coverage` 실행
2. 없고 `.ts/.tsx` 파일 있으면 `npx jest --coverage` 시도
3. `.py` 파일 있으면 `pytest --cov` 시도
4. 출력에서 커버리지 % 추출 (정규식) → `THRESHOLD` 와 비교
5. 통과/실패 + 현재 % 리포트

## 설정
- `PROJECT_PATH`: 검사할 프로젝트 루트
- `THRESHOLD`: 최소 커버리지 % (기본 `80`)

## 한계
- 커버리지 도구 미설치 시 실패 — `jest`, `pytest-cov` 사전 설치 필요
- % 추출은 정규식 기반 — 비표준 출력 포맷이면 파싱 실패 가능
- 파일별 세부 커버리지 미제공, 전체 합산 수치만 비교
