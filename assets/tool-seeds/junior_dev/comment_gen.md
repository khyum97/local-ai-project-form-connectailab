<!-- version: comment_gen_v1 -->
# 🌱 comment_gen — JSDoc / docstring 주석 뼈대 생성

연아가 함수·클래스 파일 작성 후 호출 → 소스 파일 파싱하여 주석 없는 함수에 JSDoc/docstring 뼈대 삽입.

## 동작
1. `SOURCE_FILE` 읽기
2. 주석 없는 함수·메서드·클래스 감지
3. JSDoc(TS/JS) 또는 docstring(Python) 뼈대 삽입한 파일을 `{원본명}.commented.ts` 로 저장

## 설정
- `SOURCE_FILE`: 주석을 추가할 소스 파일 (절대 또는 프로젝트 상대 경로)
- `PROJECT_PATH`: 프로젝트 루트 (상대 경로 기준)

## 한계
- 단순 정규식 파싱 — 복잡한 제네릭·데코레이터 누락 가능
- 원본 파일 수정 없음 — `.commented.` 파일로 출력, 수동으로 검토 후 적용
