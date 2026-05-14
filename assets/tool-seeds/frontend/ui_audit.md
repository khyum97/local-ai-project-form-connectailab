<!-- version: ui_audit_v1 -->
# ui_audit — 프론트엔드 코드 품질 감사

지아가 PR 전이나 코드 리뷰 전 호출 → .tsx/.jsx 파일 전체를 스캔해 품질 이슈 리포트 생성.

## 동작
1. `PROJECT_PATH` 하위의 `.tsx` / `.jsx` 파일 재귀 탐색 (node_modules / dist 제외)
2. 파일별로 아래 항목 grep 검사:
   - **aria 속성 누락**: `<img` 태그에 `alt=` 없음, `<button` 에 accessible label 없음
   - **console.log 잔존**: `console.log(` 패턴
   - **any 타입 사용**: `: any` / `as any` 패턴
   - **TODO/FIXME 태그**: `// TODO` / `// FIXME` 주석
3. 파일별 이슈 목록을 마크다운 리포트로 출력
4. 이슈 없으면 ✅ 클린 상태 출력

## 설정
- `PROJECT_PATH`: 감사할 프로젝트 루트 폴더
- `STRICT`: `true` 면 이슈 발견 시 exit code 1 반환 (CI 연동용). 기본 `false`

## 한계
- AST 분석이 아닌 단순 문자열 grep — 오탐(false positive) 가능
- aria 감사는 일부 패턴만 커버 (완전한 접근성 감사 아님)
- 자동 수정 없음 — 보고만 함
