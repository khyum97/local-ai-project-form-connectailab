<!-- version: log_monitor_v1 -->
# 🚀 log_monitor — 로그 패턴 분석

서준이 서비스 운영 중 호출 → 로그 파일에서 에러·경고·이상 패턴 스캔 후 요약 리포트.

## 동작
1. `LOG_FILE` 또는 `LOG_DIR` 에서 최신 로그 파일 읽기
2. ERROR·WARN·FATAL 패턴 카운트
3. 반복 에러 TOP 5 추출
4. 마지막 `TAIL_LINES`줄 미리보기

## 설정
- `LOG_FILE`: 단일 로그 파일 경로 (우선)
- `LOG_DIR`: 로그 디렉토리 (최신 .log 파일 자동 선택)
- `TAIL_LINES`: 미리보기 줄 수 (기본 20)

## 한계
- JSON 로그·구조화 로그 부분 지원
- 실시간 스트리밍 없음 — 스냅샷 분석만
