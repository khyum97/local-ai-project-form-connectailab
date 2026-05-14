<!-- version: bug_report_v1 -->
# 🧪 bug_report — 버그 리포트 마크다운 템플릿 생성

유나가 버그 발견 시 호출 → 표준 버그 리포트 마크다운 파일 자동 생성.

## 동작
1. `BUG_TITLE`·`SEVERITY`·`ENVIRONMENT` 읽기
2. 표준 섹션 포함 마크다운 생성:
   - 재현 절차, 기대 동작, 실제 동작, 환경 정보, 첨부 파일 란
3. `PROJECT_PATH/docs/bugs/YYYYMMDD_{slug}.md` 로 저장

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `BUG_TITLE`: 버그 제목
- `SEVERITY`: `critical` | `high` | `medium` | `low` (기본 `medium`)
- `ENVIRONMENT`: 환경 설명 (예: `Chrome 124, macOS 14, staging`)

## 한계
- 재현 절차·기대 동작은 수동 작성 필요
