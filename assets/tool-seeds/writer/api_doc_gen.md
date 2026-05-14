<!-- version: api_doc_gen_v1 -->
# 📝 api_doc_gen — API 문서 자동 생성

Writer가 백엔드 라우트 파일을 확인한 후 호출 → Express·FastAPI 라우트 파싱 → 마크다운 API 레퍼런스 생성.

## 동작
1. `SOURCE_FILE` 에서 HTTP 메서드·경로 패턴 추출
   - Express: `router.(get|post|put|patch|delete)(path, ...)`
   - FastAPI: `@app.(get|post|put|patch|delete)(path)`
2. 엔드포인트별 섹션 생성 (메서드, 경로, 파라미터 TODO, 응답 TODO)
3. `PROJECT_PATH/docs/api/{파일명}.md` 로 저장

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `SOURCE_FILE`: 라우트 파일 경로 (예: `src/routes/users.ts`)
- `API_PREFIX`: API 경로 prefix (예: `/api/v1`, 기본 빈 문자열)

## Writer 권장 흐름
```
1. backend 팀이 라우트 파일 구현 완료
2. <run_command>python3 .../api_doc_gen.py</run_command>
3. 생성된 docs/api/*.md 에서 파라미터·응답 스키마 보완
```

## 한계
- 파라미터·요청 바디 스키마는 TODO — 수동 보완 필요
- 미들웨어 체인 내 중첩 라우터는 감지 안 됨
