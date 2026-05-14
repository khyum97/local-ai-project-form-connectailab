<!-- version: task_breakdown_v1 -->
# 🧭 task_breakdown — 작업 분해 및 에이전트 배분

CEO가 큰 기능 요청을 받았을 때 호출 → 서브태스크로 분해 → 담당 에이전트와 순서 출력.

## 동작
1. `TASK_DESC` 에서 요구사항 읽기
2. 작업을 논리 단위로 분해 (최대 `MAX_SUBTASKS`개)
3. 각 서브태스크에 담당 에이전트 ID 배정:
   - 아키텍처/설계 결정 → senior_dev
   - UI 컴포넌트·화면 → frontend
   - API·DB·서버 로직 → backend
   - 배포·CI 파이프라인 → devops
   - 디자인 스펙·와이어프레임 → designer
   - 테스트·품질 검증 → qa
   - 문서화 → writer
   - 기술 조사·비교 → researcher
   - 보일러플레이트·반복 코드 → junior_dev
4. 마크다운 테이블 형태로 출력

## 설정
- `TASK_DESC`: 분해할 작업 설명 (자유 텍스트)
- `MAX_SUBTASKS`: 최대 서브태스크 수 (기본 8)

## CEO 권장 흐름
```
1. 사용자 요청 수신
2. <run_command>python3 .../task_breakdown.py</run_command>
3. 출력된 서브태스크 목록을 각 에이전트에 순서대로 전달
```

## 한계
- 자동 에이전트 실행 없음 — CEO가 직접 결과 보고 분배 판단
- 복잡한 의존 관계는 수동으로 순서 조정 필요
