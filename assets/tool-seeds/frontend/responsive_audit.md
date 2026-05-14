<!-- version: responsive_audit_v1 -->
# 🎯 responsive_audit — 반응형 CSS 점검

지아가 컴포넌트 구현 후 호출 → CSS/Tailwind 파일에서 반응형 이슈 패턴 정적 스캔 → 리포트 출력.

## 동작
1. `PROJECT_PATH/src` 내 `.css`, `.tsx`, `.jsx`, `.vue` 파일 스캔
2. 반응형 이슈 패턴 감지:
   - 고정 px 너비 (`width: \d+px` — 단, 2px·4px 등 소형 제외)
   - `position: fixed`/`absolute` 없는 overflow 설정
   - Tailwind 반응형 prefix(`sm:`·`md:`·`lg:`) 없는 레이아웃 클래스
3. 파일·줄 번호·패턴 종류 마크다운 리포트 출력

## 설정
- `PROJECT_PATH`: 스캔할 프로젝트 루트

## 한계
- 정적 스캔만 — 실제 브라우저 렌더링 검증 아님
- Tailwind JIT 동적 클래스 감지 불가
