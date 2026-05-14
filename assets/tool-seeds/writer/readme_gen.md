<!-- version: readme_gen_v1 -->
# 📝 readme_gen — README.md 자동 생성

Writer가 프로젝트 분석 후 호출 → `package.json`·소스 구조를 읽어 README.md 초안 생성.

## 동작
1. `PROJECT_PATH/package.json` 에서 name·description·version·scripts 읽기
2. `src/` 폴더 구조 스캔 (최대 2단계)
3. 템플릿 섹션 자동 채움: 개요·설치·사용법·스크립트·구조·라이선스
4. `PROJECT_PATH/README.md` 로 저장 (기존 파일 있으면 README.draft.md 로 저장)

## 설정
- `PROJECT_PATH`: README를 생성할 프로젝트 루트
- `LANG`: `ko` | `en` (기본 `ko`)

## Writer 권장 흐름
```
1. 프로젝트 기능 파악 (CEO / senior_dev 협의)
2. <run_command>python3 .../readme_gen.py</run_command>
3. 생성된 README.md 에서 TODO 항목 직접 채워 완성
```

## 한계
- 프로젝트 기능 설명은 TODO 로 남음 — 작성자가 직접 보완 필요
- package.json 없으면 기본 구조만 생성
