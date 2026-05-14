<!-- version: dockerfile_gen_v1 -->
# dockerfile_gen — Dockerfile 자동 생성

서준이 프로젝트 타입을 감지하거나 설정을 읽어 Dockerfile과 .dockerignore를 자동 생성한다.

## 동작
1. `APP_TYPE` 에 따라 베이스 이미지·빌드 전략 결정
   - `node`: `node:20-alpine` 기반, npm ci + 빌드 멀티스테이지
   - `python`: `python:3.12-slim` 기반, pip install requirements.txt
   - `static`: `nginx:alpine` 기반, 정적 파일 서빙
2. `BASE_IMAGE` 지정 시 해당 이미지로 오버라이드
3. `OUTPUT_PATH` 에 `Dockerfile` + `.dockerignore` 생성

## 설정
- `PROJECT_PATH`: 프로젝트 루트 경로 (필수)
- `APP_TYPE`: `'node'` | `'python'` | `'static'` (필수)
- `PORT`: 노출 포트 (기본 `3000`)
- `BASE_IMAGE`: 베이스 이미지 오버라이드 (선택)
- `OUTPUT_PATH`: 출력 경로 (기본 `PROJECT_PATH`)

## 한계
- 멀티스테이지 빌드는 node 타입만 지원
- Kubernetes / docker-compose 파일은 별도 도구 사용
- 비표준 패키지 관리자(yarn berry, pnpm 등)는 수동 조정 필요
