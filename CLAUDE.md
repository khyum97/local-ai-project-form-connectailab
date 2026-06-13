# Yum Agent Company — Claude 작업 지침

## 버전 관리 규칙

**이 프로젝트를 수정할 때마다 `package.json`의 `version`을 반드시 올릴 것.**

버전 체계: `2.MINOR.PATCH`
- PATCH (+1): 단일 파일 소규모 수정, 버그 수정, 텍스트 변경
- MINOR (+1, PATCH 리셋): 새 에이전트 추가, 새 기능, 구조적 변경
- 현재 버전: **2.101.1**

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 2.101.1 | 2026-06-13 | 일괄 모델 적용(setAllAgents) 기능 수정(명시적 기록 및 대시보드 실시간 동기화) 및 대시보드 내 일괄 변경 편의 기능 추가 |
| 2.101.0 | 2026-06-13 | 신규 에이전트 4종(주식/시장/음성/블로그) 및 권한 제한 정책 수립, 검수 게이트 실제 코드 변경 검증 및 반려 경고 주입 기능 구현 |
| 2.100.3 | 2026-05-20 | LLM 출력 스트림 무한 루프 가드 추가 및 비정상 파일 편집 반복 방지 |
| 2.100.2 | 2026-05-20 | 슬래시 명령어 카드 웹뷰 대기 락 버그 수정 및 에이전트 구상 반복 방지 대책 적용 |
| 2.100.0 | 2026-05-15 | 입력창 명령어 카드 패널 추가; `/` 입력 또는 명령 버튼으로 command registry 관리 |
| 2.99.0 | 2026-05-15 | Factory Queue `/factory seed` 추가; 빈 큐일 때 활성 프로젝트 기반 기본 생산 티켓 생성 |
| 2.98.0 | 2026-05-15 | Factory Queue `/factory auto` 상시 루프 추가; running 상태에서 review 후 tick 자동 enqueue |
| 2.97.0 | 2026-05-15 | Factory Queue `/factory review` 추가; evidence 있는 review 티켓을 shipped로 승격하고 부족하면 blocked 처리 |
| 2.96.0 | 2026-05-15 | Factory Queue `/factory tick` 실행 추가; 첫 backlog 티켓을 CEO 디스패치로 보내고 evidence 기록 |
| 2.95.0 | 2026-05-15 | Project Workspace Manager와 Factory Queue MVP 추가; 자연어 Skill Pack 토글 및 README 명령어 정리 |
| 2.94.0 | 2026-05-15 | Skill Pack Manager MVP 추가; Caveman/Superpowers pack을 회사 에이전트 prompt에 토글 주입 |
| 2.93.0 | 2026-05-15 | 13명 개발회사 UI·라우팅·툴 카탈로그 정렬; 새 개발팀 tool-seeds와 빌드/권한 예시 정리 |
| 2.92.2 | 2026-05-14 | Agent roster cleaned to 13 agents; accountant/lawyer made general business experts; Skill Library auto-seeds all bundled tool-seeds |
| 2.92.1 | 2026-05-14 | Build scripts made ASCII-safe; package manifest text normalized to avoid Korean encoding build issues |
| 2.92.0 | 2026-05-13 | DevOps, QA, JuniorDev, Secretary, senior_dev, accountant, lawyer tool-seeds added |
| 2.91.0 | 2026-05-13 | CEO 툴 시드 4개 추가 (task_breakdown, decision_log) |
| 2.90.3 | 2026-05-13 | 새 에이전트 픽셀 스프라이트 추가 (frontend/backend/devops/qa/junior_dev/senior_dev) |
| 2.90.2 | 2026-05-13 | junior_dev PIN 잠금 제거 → DEFAULT_ON 정상 에이전트로 전환 |
| 2.90.1 | 2026-05-13 | extension.ts 내 "Connect AI" 표시 문자열 → "Yum Agent Company" |
| 2.90.0 | 2026-05-13 | 팀 전면 재구성 (유튜브→개발팀 11명), 프로그램 이름 → Yum Agent Company |
| 2.89.157 | (이전) | 기존 Connect AI Lab 마지막 버전 |

---

## 프로젝트 구조 핵심

- **에이전트 정의**: `src/agents.ts` — AGENTS 맵, AGENT_ORDER, SPECIALIST_IDS
- **라우팅 프롬프트**: `assets/prompts/ceo-classifier.md`, `ceo-planner.md`, `confer.md`
- **에이전트 목표**: `src/extension.ts` 내 `DEFAULT_AGENT_GOALS` (줄 6100 근처)
- **툴 시드**: `assets/tool-seeds/{agent_id}/` — .md(설명) + .py(구현)
- **시스템 프롬프트**: `assets/prompts/system.md`
- **빌드**: `build.bat` (더블클릭) 또는 `build.ps1` → `yum-agent-company-{version}.vsix`

## 현재 팀 구성

| ID | 이름 | 역할 |
|----|------|------|
| `ceo` | CEO | CTO·오케스트레이터 |
| `senior_dev` | 코다리 | 시니어 풀스택 |
| `frontend` | 지아 | 프론트엔드 |
| `backend` | 민준 | 백엔드 |
| `devops` | 서준 | DevOps |
| `designer` | Designer | UI/UX |
| `qa` | 유나 | QA |
| `writer` | Writer | 기술 문서 |
| `researcher` | Researcher | 기술 조사 |
| `secretary` | 영숙 | 비서 |
| `junior_dev` | 연아 | 주니어 개발자 |
| `accountant` | 재무 | 재무·회계 전문가 |
| `lawyer` | 법무 | 법무·컴플라이언스 전문가 |

## 주의사항

- `connectAiLab.*` 설정 키 — **변경 금지** (사용자 VS Code 설정 날아감)
- command ID (`connect-ai-lab.*`) — 변경 시 extension.ts 전체 영향
- `extension.ts` 21,721줄 — 편집 시 반드시 해당 줄 Read 확인 후 정확한 텍스트로 Edit
- 빌드 전 항상 버전 올릴 것
