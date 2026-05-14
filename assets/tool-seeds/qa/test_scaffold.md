<!-- version: test_scaffold_v1 -->
# 🧪 test_scaffold — 테스트 파일 자동 생성

유나가 소스 파일을 확인한 직후 호출 → 프레임워크별 테스트 뼈대 자동 생성 → 3개 기본 케이스 포함.

## 동작
1. `TARGET_FILE` 로부터 기본 파일명 추출 (확장자·경로 제거)
2. `TEST_FRAMEWORK` 에 따라 출력 경로·형식 결정:
   - `jest` → `__tests__/{파일명}.test.ts` (describe/it 구조)
   - `pytest` → `tests/test_{파일명}.py`
   - `playwright` → `e2e/{파일명}.spec.ts`
3. happy path / edge case / error case 3개 기본 케이스 포함
4. 생성된 파일 경로 출력

## 설정
- `PROJECT_PATH`: 테스트를 생성할 프로젝트 루트
- `TEST_FRAMEWORK`: `jest` | `pytest` | `playwright` (기본 `jest`)
- `TARGET_FILE`: 테스트 대상 소스 파일 경로 (예: `src/utils/format.ts`)

## 한계
- 실제 함수 시그니처 분석 없이 뼈대만 생성 — 구체적 단언(assertion)은 수동 작성 필요
- 기존 테스트 파일 있으면 덮어쓰지 않고 경고 후 종료
- `playwright` 는 e2e/ 폴더가 프로젝트에 없어도 생성 시도
