<!-- version: deploy_check_v1 -->
# deploy_check — 배포 상태 확인

서준이 배포 후 대상 URL에 HTTP GET 요청을 보내 상태 코드·응답 시간·헤더를 확인한다.

## 동작
1. `TARGET_URL` 에 HTTP GET 요청 (urllib.request 사용, 외부 의존성 없음)
2. 응답 상태 코드를 `EXPECTED_STATUS` 와 비교
3. 응답 시간(ms) 측정
4. 주요 응답 헤더 요약 출력
5. 성공/실패 여부 + 상세 결과 리포트

## 설정
- `TARGET_URL`: 확인할 URL (필수, 예: `https://example.com`)
- `EXPECTED_STATUS`: 기대 HTTP 상태 코드 (기본 `200`)
- `TIMEOUT_SECONDS`: 요청 타임아웃 초 (기본 `10`)

## 한계
- HTTPS 인증서 오류 시 실패 처리 (verify 강제)
- POST/PUT 등 다른 메서드 미지원
- 리다이렉트는 최대 3회까지 자동 추적
