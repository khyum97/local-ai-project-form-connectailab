<!-- version: decision_log_v1 -->
# 🧭 decision_log — 기술 결정 기록

CEO가 기술 방향을 결정했을 때 호출 → `_shared/decisions.md` 에 결정 사항 누적 기록.

## 동작
1. `DECISION_TITLE`, `DECISION_BODY`, `ALTERNATIVES` 읽기
2. 타임스탬프 포함 결정 블록 생성
3. `BRAIN_PATH/_shared/decisions.md` 에 최신 항목을 파일 상단에 추가
4. 기존 파일 없으면 새로 생성

## 설정
- `BRAIN_PATH`: 두뇌 폴더 경로 (기본 `~/.connect-ai-brain`)
- `DECISION_TITLE`: 결정 제목 (예: "인증 라이브러리 선택")
- `DECISION_BODY`: 결정 내용 및 이유
- `ALTERNATIVES`: 검토했지만 선택하지 않은 대안들 (쉼표 구분)

## CEO 권장 흐름
```
1. 기술 스택/아키텍처 결정 완료
2. <run_command>python3 .../decision_log.py</run_command>
3. decisions.md 가 자동 갱신됨 → Git 자동 동기화로 기록 보존
```

## 한계
- Git 커밋은 별도 — 자동 동기화(_safeGitAutoSync)가 처리
- 결정 수정은 파일 직접 편집 필요
