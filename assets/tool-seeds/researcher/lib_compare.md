<!-- version: lib_compare_v1 -->
# 🔍 lib_compare — 라이브러리 비교 리포트 생성

Researcher가 기술 스택 결정 전 호출 → 후보 라이브러리들을 비교 매트릭스 마크다운으로 정리.

## 동작
1. `CANDIDATES` 목록 읽기 (쉼표 구분)
2. `CRITERIA` 기준별로 비교 매트릭스 표 생성
3. npm/PyPI 최신 버전·주간 다운로드 수 확인 (네트워크 가능 시)
4. 결론 섹션에 추천 라이브러리 + 근거 TODO 포함
5. `PROJECT_PATH/docs/research/{주제}.md` 로 저장

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `TOPIC`: 비교 주제 (예: `state-management`, `orm`)
- `CANDIDATES`: 비교할 라이브러리 (쉼표 구분, 예: `zustand,redux,jotai`)
- `CRITERIA`: 비교 기준 (쉼표 구분, 기본: `번들크기,학습곡선,생태계,TypeScript지원,유지보수`)

## Researcher 권장 흐름
```
1. CEO 또는 senior_dev 에게 기술 조사 요청 수신
2. <run_command>python3 .../lib_compare.py</run_command>
3. 생성된 마크다운에서 각 셀 직접 채워 완성
4. CEO 에게 결과 보고
```

## 한계
- 자동 채워지는 수치는 npm registry API 기준 (네트워크 필요)
- 네트워크 없으면 TODO 셀로 대체
- 주관적 평가 (학습곡선 등)는 수동 작성 필요
