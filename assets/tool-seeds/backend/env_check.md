<!-- version: env_check_v1 -->
# 🔐 env_check — 환경변수 검증 도구

민준이 배포 전 또는 개발 환경 세팅 시 호출 → `.env.example` 대비 누락 키 리포트.

## 동작
1. `PROJECT_PATH/.env.example` 읽어서 필수 키 목록 추출 (주석·빈 줄 제외)
2. `PROJECT_PATH/.env` 파싱 (없으면 `os.environ` 사용)
3. `.env.example` 키 중 현재 환경에 없는 키를 누락 목록으로 리포트
4. 누락 없으면 통과, 있으면 목록 출력 후 exit code 1

## 설정
- `PROJECT_PATH`: 검사할 프로젝트 경로 (필수)
- `ENV_FILE`: 비교할 env 파일명 (기본 `.env`, `.env.local` 등 지정 가능)

## 한계
- 값 검증 없음 — 키 존재 여부만 확인 (빈 값도 존재로 간주)
- dotenv 라이브러리 미사용 — `KEY=VALUE` 형식만 지원, 멀티라인 값 미지원
- `.env.example` 파일 없으면 검사 불가
