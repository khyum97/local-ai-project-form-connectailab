<!-- version: component_scaffold_v1 -->
# component_scaffold — React/TypeScript 컴포넌트 보일러플레이트 생성기

지아가 React 컴포넌트를 새로 만들 때 호출 → Props 인터페이스 + 기본 구조 자동 생성.

## 동작
1. `COMPONENT_NAME` 기반으로 `{ComponentName}.tsx` 파일 생성
2. `TYPE` 에 따라 함수형(`function`) 또는 `forwardRef` 컴포넌트 구조 선택
3. `CSS_MODE` 에 따라 Tailwind className / CSS Module styles / 빈 plain 중 하나 삽입
4. `OUTPUT_DIR` 폴더 없으면 자동 생성 (`os.makedirs`)
5. 생성 경로 + 파일 내용 요약 리포트 출력

## 설정
- `COMPONENT_NAME`: 컴포넌트 이름 (PascalCase 권장, 예: `UserCard`)
- `TYPE`: `'function'` (기본) 또는 `'forwardRef'`
- `CSS_MODE`: `'tailwind'` (기본) | `'module'` | `'plain'`
- `OUTPUT_DIR`: 생성 위치 (예: `src/components`)

## 한계
- 복잡한 비즈니스 로직은 포함하지 않음 — 뼈대만 생성
- 이미 파일이 존재하면 덮어쓰지 않고 경고 후 종료
- CSS Module 파일(`.module.css`)은 별도로 생성하지 않음
