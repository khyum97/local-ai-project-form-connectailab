<!-- version: stack_audit_v1 -->
# 🔍 stack_audit — 프로젝트 기술 스택 분석

Researcher가 기존 프로젝트 분석 시 호출 → 의존성·버전·잠재적 이슈를 마크다운 리포트로 정리.

## 동작
1. `package.json` (Node) 또는 `requirements.txt` (Python) 읽기
2. 각 의존성 분류: 런타임 / 개발 / 미분류
3. 메이저 버전 고정 여부, deprecated 패키지 경고 패턴 감지
4. `PROJECT_PATH/docs/research/stack-audit.md` 로 저장

## 설정
- `PROJECT_PATH`: 분석할 프로젝트 루트

## Researcher 권장 흐름
```
1. 신규 프로젝트 온보딩 또는 리팩토링 전
2. <run_command>python3 .../stack_audit.py</run_command>
3. 출력된 리포트를 CEO·senior_dev 에게 공유
```

## 한계
- 실제 보안 취약점 스캔 없음 (`npm audit` 별도 실행 필요)
- Python requirements.txt 만 지원 (pyproject.toml 미지원)
