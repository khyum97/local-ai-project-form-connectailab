<!-- version: a11y_check_v1 -->
# 🎯 a11y_check — 접근성(Accessibility) 정적 점검

지아가 UI 구현 후 호출 → JSX/TSX/HTML 파일에서 WCAG 기본 항목 정적 스캔.

## 동작
1. `PROJECT_PATH/src` 내 `.tsx`, `.jsx`, `.html` 파일 스캔
2. 감지 항목:
   - `<img>` `alt` 속성 누락
   - `<button>` 텍스트·`aria-label` 누락
   - `<input>` `id`·`aria-label`·`htmlFor` 없음
   - `tabIndex` 음수 사용
   - 색상 대비 주석 누락 경고 (manual reminder)
3. 파일·줄·이슈 마크다운 리포트

## 설정
- `PROJECT_PATH`: 스캔할 프로젝트 루트

## 한계
- 정적 텍스트 스캔 — 동적 생성 JSX 완전 감지 불가
- 색상 대비는 자동 계산 불가 (수동 확인 필요)
