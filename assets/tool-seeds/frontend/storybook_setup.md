<!-- version: storybook_setup_v1 -->
# storybook_setup — Storybook 초기 설정 자동화

지아가 새 프로젝트에 Storybook을 세팅할 때 호출 → `npx storybook@latest init` 실행 + 결과 보고.

## 동작
1. `PROJECT_PATH` 폴더에서 `npx storybook@latest init --yes` 실행
2. 실행 전 `package.json` 존재 여부 확인 (Node 프로젝트인지 검증)
3. 설치 stdout/stderr 캡처 → 성공/실패 판별
4. 완료 후 설치 결과 마크다운 리포트 출력
5. 실패 시 마지막 30줄 로그 포함하여 원인 파악 지원

## 설정
- `PROJECT_PATH`: Storybook을 설치할 프로젝트 루트 폴더
- `TIMEOUT`: 명령 타임아웃(초). 기본 300 (5분)

## 한계
- 인터랙티브 프롬프트가 발생하는 환경에서는 `--yes` 플래그 있어도 중단될 수 있음
- 이미 Storybook이 설치된 경우 재설치 방지 로직 없음 — 직접 확인 필요
- 네트워크 환경에 따라 타임아웃 조정 필요
