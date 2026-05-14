# Agent Safety Notes

작성일: 2026-05-14

## 결론

어제 하루 종일 돌린 결과가 망가진 이유는 로컬 LLM 성능만의 문제가 아니다.

작은 모델은 긴 자율 작업에서 코드와 문서를 섞고, 없는 API를 가정하고, 검증 없이 완료라고 말하기 쉽다. 하지만 더 큰 모델을 써도 실행기 쪽에 검증 게이트가 없으면 비슷한 문제가 반복된다.

현재 문제 비중은 대략 다음처럼 보는 것이 맞다.

- 모델 성능/컨텍스트 한계: 40%
- 실행기의 제약/검증 부족: 60%

## 발견된 실제 문제

- `E:\AI기업 (주)경흥\src\workers\compensation_worker.py` 안에 `<create_file ...>` 태그가 그대로 들어가 Python 문법 오류가 발생했다.
- `E:\AI기업 (주)경흥\src\services\order_lookup_service.py`도 같은 유형의 문법 오류가 있었다.
- 테스트 파일은 실제 구현과 맞지 않는 가짜 인터페이스를 기준으로 작성됐다.
- 여러 보고서와 메모리에 인코딩 깨짐이 있었다.
- 작업 목표가 `주식 자동매매`에서 `Saga/Outbox/장애 모니터링`으로 흘러가며 드리프트가 생겼다.

## 적용한 개선

`src/agentOutputGuard.ts`를 추가해 저장 전 검증 게이트를 만들었다.

검증 게이트가 막는 것:

- 코드 파일 안에 `<create_file>`, `<edit_file>`, `<run_command>` 같은 액션 태그가 들어가는 경우
- 코드 파일 안에 markdown code fence가 남는 경우
- `.py` 파일이 `python -m py_compile`을 통과하지 못하는 경우
- `.json` 파일이 JSON 파싱을 통과하지 못하는 경우

연결된 저장 경로:

- 일반 `<create_file>` 저장
- `<edit_file>`로 수정 후 저장
- markdown fallback 자동 파일 생성
- 외부 skill/script injection의 `.py` 저장
- template injection의 code-like 파일 저장

## 추가된 검증 명령

- `npm run test:guard`
- `npm run test:agent-safety`

## 앞으로 더 해야 할 일

1. 장시간 auto-cycle 제한: 한 사이클은 15~30분, 파일 1~3개, 테스트 1개 통과 단위로 제한.
2. 완료 조건 강화: 수정 파일, 검증 명령, exit code, 실패 원인, 다음 작업을 강제.
3. 역할 분리: CEO는 분해, Builder는 작성, Verifier는 실제 명령 실행.
4. 코드와 초안 분리: `sessions/`는 설계/초안, `src/`는 검증 통과 코드만.
5. 모델 역할 조정: Gemma e4b는 초안/요약/분류용, 실제 코드는 coder 모델 권장.

## 운영 원칙

- 자동 작성보다 자동 검증이 먼저다.
- 검증 실패 파일은 `src/`에 저장하지 않는다.
- 보고서가 길어지는 것은 진척이 아니다. 실행 가능한 테스트가 진척이다.
- 완료는 LLM 판단이 아니라 명령 결과로 판단한다.
