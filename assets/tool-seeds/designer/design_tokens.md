<!-- version: design_tokens_v1 -->
# 🎨 design_tokens — 디자인 토큰 파일 생성

Designer가 새 프로젝트나 디자인 시스템 초기화 시 호출 → colors·spacing·typography 토큰 파일 자동 생성.

## 동작
1. `STYLE` 에 따라 색상 팔레트 선택 (modern-dark / modern-light / corporate)
2. `PROJECT_PATH` 아래 `src/styles/tokens.css` 생성 (CSS 변수)
3. Tailwind 프로젝트이면 `tailwind.config.js` 에 주입할 `theme.extend` 스니펫도 출력

## 설정
- `PROJECT_PATH`: 토큰을 생성할 프로젝트 루트
- `STYLE`: `modern-dark` | `modern-light` | `corporate` (기본 `modern-dark`)
- `TAILWIND`: `true` 면 tailwind 스니펫 추가 출력

## Designer 권장 흐름
```
1. 프로젝트 스택 파악 (frontend 팀 협의)
2. <run_command>python3 .../design_tokens.py</run_command>
3. 생성된 tokens.css 를 컴포넌트에서 var(--color-primary) 형태로 사용
```

## 한계
- 기존 tokens.css 있으면 덮어쓰지 않고 경고
- Tailwind 자동 주입 없음 — 스니펫 복사해서 수동으로 tailwind.config.js 에 붙여넣기
