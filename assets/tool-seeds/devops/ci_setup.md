<!-- version: ci_setup_v1 -->
# ci_setup — GitHub Actions CI 워크플로 생성

서준이 프로젝트 타입에 맞는 GitHub Actions CI 워크플로를 `.github/workflows/ci.yml` 에 자동 생성한다.

## 동작
1. `WORKFLOW_TYPE` 에 따라 워크플로 템플릿 결정
   - `node-test`: Node 20 설치 → `npm ci` → `npm test`
   - `python-test`: Python 3.12 설치 → `pip install -r requirements.txt` → `pytest`
   - `docker-build`: `docker build` + 이미지 태그 (SHA 기반)
2. `BRANCH` 에 push/pull_request 트리거 설정
3. `PROJECT_PATH/.github/workflows/ci.yml` 파일 생성

## 설정
- `PROJECT_PATH`: 프로젝트 루트 경로 (필수)
- `WORKFLOW_TYPE`: `'node-test'` | `'python-test'` | `'docker-build'` (필수)
- `BRANCH`: 트리거 브랜치 (기본 `'main'`)

## 한계
- GitHub Secrets 설정은 수동으로 해야 함
- 모노레포 구조는 별도 조정 필요
- self-hosted runner 미지원 (GitHub-hosted runner 기준)
