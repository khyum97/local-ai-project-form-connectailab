<!-- version: boilerplate_gen_v1 -->
# 🏗️ boilerplate_gen — 보일러플레이트 파일 자동 생성

연아가 새 모듈·훅·서비스 시작 전 호출 → 템플릿 선택 → 파일 즉시 생성 → 경로 출력.

## 동작
1. `TEMPLATE_TYPE` 에 따라 생성 파일 결정:
   - `util-function` → `{OUTPUT_DIR}/{NAME}.ts` (TypeScript 유틸 함수)
   - `hook` → `{OUTPUT_DIR}/use{Name}.ts` (React Hook 뼈대)
   - `service` → `{OUTPUT_DIR}/{Name}Service.ts` (서비스 클래스)
   - `config` → `{OUTPUT_DIR}/{name}.json` + `{OUTPUT_DIR}/.env.example`
2. `OUTPUT_DIR` 없으면 자동 생성
3. 기존 파일 있으면 경고 후 덮어쓰지 않음
4. 생성된 파일 절대 경로 출력

## 설정
- `TEMPLATE_TYPE`: `util-function` | `hook` | `service` | `config`
- `NAME`: 생성할 파일/심볼 이름 (예: `formatDate`, `Auth`, `database`)
- `OUTPUT_DIR`: 파일을 생성할 디렉터리 경로

## 한계
- 템플릿은 정적 뼈대 — 비즈니스 로직은 수동 작성 필요
- TypeScript 전용 (`util-function`, `hook`, `service`) — JS 변환 미지원
- `config` 는 `.env.example` 키 목록이 고정 예시 — 프로젝트에 맞게 수정 필요
