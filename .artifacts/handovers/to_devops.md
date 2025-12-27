# Handovers: To DevOps

## 날짜
2025-12-27

## 브랜치 (Version Control)
- N/A

## 현재 상황 (Context)
- v0.7.0 완료. v0.8.0(Authentication) 준비 중입니다.
- 인증 도입 시 이메일 발송(비밀번호 찾기 등)이 필수적이므로 기존 메일 인프라 점검이 필요합니다.

## 해야 할 일 (Tasks)
1. 비밀번호 해싱 등을 위한 시스템 레벨 의존성(예: `libffi-dev`, `python3-dev` 등)이 Docker 이미지에 누락되어 있는지 확인. (보통은 Python 이미지에 포함되나 확인 필요)
2. 현재 구축된 Celery + Redis + SMTP 파이프라인이 "비밀번호 재설정 이메일" 발송에도 즉시 사용 가능한지 확인.
   - 별도의 Rate Limit 정책이 필요한지 고려.

## 기대 산출물 (Expected Outputs)
- 특별한 변경사항 없으면 "이상 없음" 리포트.
- 추가 패키지 필요 시 `Dockerfile` 또는 `docker-compose.yml` 수정 제안.

## 참고 자료 (References)
- `.artifacts/contexts/devops.md`
