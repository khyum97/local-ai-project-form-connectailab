#!/usr/bin/env python3
# version: design_tokens_v1
"""디자인 토큰 파일 생성 — CSS 변수 + Tailwind 스니펫 출력.

config:
  PROJECT_PATH — 프로젝트 루트
  STYLE        — 'modern-dark' | 'modern-light' | 'corporate' (기본 modern-dark)
  TAILWIND     — 'true' 면 tailwind theme.extend 스니펫도 출력
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "design_tokens.json")

PALETTES = {
    "modern-dark": {
        "primary": "#6366F1",
        "primary-hover": "#4F46E5",
        "secondary": "#22D3EE",
        "accent": "#F472B6",
        "background": "#0F172A",
        "surface": "#1E293B",
        "surface-2": "#334155",
        "text": "#F8FAFC",
        "text-muted": "#94A3B8",
        "border": "#334155",
        "success": "#34D399",
        "warning": "#FBBF24",
        "error": "#F87171",
    },
    "modern-light": {
        "primary": "#6366F1",
        "primary-hover": "#4F46E5",
        "secondary": "#0EA5E9",
        "accent": "#EC4899",
        "background": "#FFFFFF",
        "surface": "#F8FAFC",
        "surface-2": "#F1F5F9",
        "text": "#0F172A",
        "text-muted": "#64748B",
        "border": "#E2E8F0",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444",
    },
    "corporate": {
        "primary": "#1D4ED8",
        "primary-hover": "#1E40AF",
        "secondary": "#0891B2",
        "accent": "#7C3AED",
        "background": "#FFFFFF",
        "surface": "#F9FAFB",
        "surface-2": "#F3F4F6",
        "text": "#111827",
        "text-muted": "#6B7280",
        "border": "#D1D5DB",
        "success": "#059669",
        "warning": "#D97706",
        "error": "#DC2626",
    },
}

SPACING = ["0", "4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px", "96px"]
FONT_SIZES = {"xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem", "3xl": "1.875rem", "4xl": "2.25rem"}
RADII = {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"}


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


def _build_css(palette):
    lines = [":root {"]
    for k, v in palette.items():
        lines.append(f"  --color-{k}: {v};")
    for i, s in enumerate(SPACING):
        lines.append(f"  --spacing-{i}: {s};")
    for k, v in FONT_SIZES.items():
        lines.append(f"  --font-{k}: {v};")
    for k, v in RADII.items():
        lines.append(f"  --radius-{k}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _build_tailwind_snippet(palette):
    color_entries = "\n".join(f"        '{k}': 'var(--color-{k})'," for k in palette)
    return f"""// tailwind.config.js — theme.extend 에 추가
theme: {{
  extend: {{
    colors: {{
{color_entries}
    }},
  }},
}},"""


def main():
    cfg = _load(CONFIG)
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or "").strip())
    if not project or not os.path.isdir(project):
        _log("PROJECT_PATH 비어있거나 존재하지 않음", "err")
        sys.exit(1)
    style = (cfg.get("STYLE") or "modern-dark").strip().lower()
    if style not in PALETTES:
        _log(f"알 수 없는 STYLE: {style}. modern-dark 사용", "warn")
        style = "modern-dark"
    tailwind = str(cfg.get("TAILWIND", "")).lower() in ("true", "1", "yes")

    palette = PALETTES[style]
    _log(f"스타일: {style}, 색상 {len(palette)}개", "info")

    out_dir = os.path.join(project, "src", "styles")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "tokens.css")

    if os.path.exists(out_path):
        _log(f"tokens.css 이미 존재 — 덮어쓰지 않음: {out_path}", "warn")
        sys.exit(1)

    _log(f"생성 중: {out_path}", "step")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(_build_css(palette))

    print()
    print(f"# ✅ 디자인 토큰 생성 완료")
    print()
    print(f"**스타일**: {style}")
    print(f"**파일**: `{out_path}`")
    print()
    print("포함된 토큰:")
    print(f"- 색상 {len(palette)}개 (`--color-*`)")
    print(f"- 간격 {len(SPACING)}단계 (`--spacing-*`)")
    print(f"- 폰트 크기 {len(FONT_SIZES)}단계 (`--font-*`)")
    print(f"- 테두리 반경 {len(RADII)}종 (`--radius-*`)")

    if tailwind:
        print()
        print("## Tailwind 스니펫")
        print()
        print("```js")
        print(_build_tailwind_snippet(palette))
        print("```")


if __name__ == "__main__":
    main()
