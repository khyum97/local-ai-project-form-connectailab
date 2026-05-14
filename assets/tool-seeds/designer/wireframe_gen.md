<!-- version: wireframe_gen_v1 -->
# 🎨 wireframe_gen — 텍스트 와이어프레임 마크다운 생성

Designer가 화면 설계 시 호출 → ASCII 레이아웃 + 컴포넌트 목록 + 인터랙션 노트 마크다운 생성.

## 동작
1. `PAGE_NAME` 과 `LAYOUT` 타입 읽기
2. 레이아웃 타입에 맞는 ASCII 와이어프레임 뼈대 생성
3. 컴포넌트 목록 (헤더/내비/콘텐츠/푸터) 자동 포함
4. `PROJECT_PATH/docs/wireframes/{PAGE_NAME}.md` 로 저장

## 설정
- `PROJECT_PATH`: 프로젝트 루트
- `PAGE_NAME`: 페이지 이름 (예: `dashboard`, `login`, `settings`)
- `LAYOUT`: `dashboard` | `auth` | `list` | `detail` (기본 `dashboard`)

## Designer 권장 흐름
```
1. 사용자 요구사항·플로우 파악
2. <run_command>python3 .../wireframe_gen.py</run_command>
3. 생성된 wireframe .md 를 frontend 팀에 전달
4. frontend 팀이 컴포넌트 구현 시 스펙 참조
```

## 한계
- ASCII 레이아웃은 구조 전달용 — 실제 픽셀 수치 없음
- Figma 연동 없음 — 마크다운 문서로만 전달
