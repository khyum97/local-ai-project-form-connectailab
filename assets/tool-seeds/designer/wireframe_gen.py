#!/usr/bin/env python3
# version: wireframe_gen_v1
"""텍스트 와이어프레임 마크다운 생성 — ASCII 레이아웃 + 컴포넌트 스펙.

config:
  PROJECT_PATH — 프로젝트 루트
  PAGE_NAME    — 페이지 이름 (예: dashboard, login)
  LAYOUT       — 'dashboard' | 'auth' | 'list' | 'detail' (기본 dashboard)
"""
import os, sys, json
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "wireframe_gen.json")

LAYOUTS = {
    "dashboard": """
┌─────────────────────────────────────────────┐
│  HEADER: 로고 + 내비 + 사용자 메뉴           │
├───────────┬─────────────────────────────────┤
│           │  📊 메트릭 카드 × 4             │
│  SIDEBAR  ├─────────────────────────────────┤
│  내비     │  📈 차트 영역                   │
│  메뉴     ├──────────────┬──────────────────┤
│           │  목록 위젯   │  활동 피드        │
└───────────┴──────────────┴──────────────────┘
""",
    "auth": """
┌─────────────────────────────────────────────┐
│  HEADER: 로고                                │
├─────────────────────────────────────────────┤
│                                             │
│         ┌──────────────────────┐            │
│         │  제목                │            │
│         │  이메일 입력          │            │
│         │  비밀번호 입력        │            │
│         │  [로그인 버튼]        │            │
│         │  소셜 로그인 옵션     │            │
│         └──────────────────────┘            │
│                                             │
└─────────────────────────────────────────────┘
""",
    "list": """
┌─────────────────────────────────────────────┐
│  HEADER: 로고 + 내비                         │
├─────────────────────────────────────────────┤
│  페이지 제목    [+ 추가 버튼]  [🔍 검색]     │
├─────────────────────────────────────────────┤
│  필터 탭: 전체 | 활성 | 비활성               │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │ 아이템 행 1 — 제목 / 설명 / 상태    │    │
│  ├─────────────────────────────────────┤    │
│  │ 아이템 행 2 — ...                   │    │
│  ├─────────────────────────────────────┤    │
│  │ 아이템 행 3 — ...                   │    │
│  └─────────────────────────────────────┘    │
│  페이지네이션: ← 1 2 3 →                    │
└─────────────────────────────────────────────┘
""",
    "detail": """
┌─────────────────────────────────────────────┐
│  HEADER: 로고 + 내비                         │
├─────────────────────────────────────────────┤
│  ← 뒤로  /  브레드크럼                       │
├───────────────────────┬─────────────────────┤
│                       │  사이드바            │
│  메인 콘텐츠 영역     │  관련 정보           │
│  (제목 + 본문)        │  액션 버튼           │
│                       │  메타데이터          │
│                       │                     │
└───────────────────────┴─────────────────────┘
""",
}

COMPONENTS = {
    "dashboard": [
        "Header: 로고, 전역 내비, 알림 아이콘, 사용자 아바타 드롭다운",
        "Sidebar: 내비 메뉴 항목, 접기/펼치기 토글",
        "MetricCard: 수치, 레이블, 변화율 배지 (×4)",
        "Chart: 시계열 라인/바 차트, 기간 필터 탭",
        "ListWidget: 최근 항목 목록, 더보기 링크",
        "ActivityFeed: 타임스탬프 + 이벤트 로그",
    ],
    "auth": [
        "Header: 로고만",
        "AuthCard: 폼 컨테이너, 섀도우, 라운드",
        "TextInput: 이메일, 비밀번호 (show/hide 토글)",
        "PrimaryButton: 로그인/가입 CTA",
        "SocialLogin: Google·GitHub OAuth 버튼",
        "TextLink: 비밀번호 찾기, 회원가입 전환",
    ],
    "list": [
        "Header: 로고, 내비, 사용자 메뉴",
        "PageHeader: 제목, 추가 버튼(Primary), 검색 인풋",
        "FilterTabs: 상태별 필터 탭 (전체/활성/비활성)",
        "ListItem: 아이콘, 제목, 부제목, 상태 배지, 액션 메뉴(⋮)",
        "EmptyState: 빈 목록 일러스트 + CTA",
        "Pagination: 이전/다음 + 페이지 번호",
    ],
    "detail": [
        "Header: 로고, 내비",
        "Breadcrumb: 계층 경로 + 뒤로가기",
        "ContentArea: 제목 H1, 본문 마크다운 렌더",
        "Sidebar: 메타데이터 카드, 액션 버튼(Primary/Secondary)",
        "RelatedList: 관련 항목 링크 목록",
    ],
}

INTERACTIONS = {
    "dashboard": ["차트 hover → 툴팁 표시", "MetricCard 클릭 → 상세 드릴다운", "Sidebar 접기 → 메인 영역 확장"],
    "auth": ["비밀번호 show/hide 토글", "폼 제출 → 로딩 스피너", "OAuth 클릭 → 팝업 플로우", "입력 오류 → 인라인 에러 메시지"],
    "list": ["검색 입력 → 실시간 필터", "항목 클릭 → Detail 페이지 이동", "추가 버튼 → 모달/슬라이드오버", "무한 스크롤 or 페이지네이션"],
    "detail": ["브레드크럼 클릭 → 상위 페이지", "액션 버튼 → 확인 다이얼로그", "사이드바 스티키 스크롤"],
}


def _log(msg, kind="info"):
    prefix = {"info": "🎨", "ok": "✅", "warn": "⚠️ ", "err": "❌", "step": "▸"}.get(kind, "•")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    page = (cfg.get("PAGE_NAME") or "page").strip().lower().replace(" ", "_")
    layout = (cfg.get("LAYOUT") or "dashboard").strip().lower()
    if layout not in LAYOUTS:
        _log(f"알 수 없는 LAYOUT: {layout}. dashboard 사용", "warn")
        layout = "dashboard"

    out_dir = os.path.join(project, "docs", "wireframes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{page}.md")

    if os.path.exists(out_path):
        _log(f"파일 이미 존재 — 덮어쓰지 않음: {out_path}", "warn")
        sys.exit(1)

    comp_list = "\n".join(f"- {c}" for c in COMPONENTS[layout])
    int_list = "\n".join(f"- {i}" for i in INTERACTIONS[layout])

    content = f"""# 🎨 와이어프레임 — {page}

> 레이아웃: `{layout}` | 생성일: {date.today().isoformat()}

## 레이아웃 구조

```
{LAYOUTS[layout].strip()}
```

## 컴포넌트 목록

{comp_list}

## 인터랙션 노트

{int_list}

## 접근성 체크리스트

- [ ] 키보드 내비게이션 지원
- [ ] ARIA 레이블 설정
- [ ] 색상 대비 4.5:1 이상 (WCAG AA)
- [ ] 포커스 인디케이터 visible
- [ ] 스크린 리더 대체 텍스트

## TODO

- [ ] 컴포넌트별 상태 (hover / active / disabled / loading) 스펙 추가
- [ ] 모바일 반응형 레이아웃 별도 작성
- [ ] 디자인 토큰 연결 (tokens.css 참조)
"""

    _log(f"생성 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"# ✅ 와이어프레임 생성 완료")
    print()
    print(f"**페이지**: {page}")
    print(f"**레이아웃**: {layout}")
    print(f"**파일**: `{out_path}`")
    print()
    print("> frontend 팀에 전달하여 컴포넌트 구현 스펙으로 활용하세요.")


if __name__ == "__main__":
    main()
