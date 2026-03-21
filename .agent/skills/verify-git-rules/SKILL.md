---
name: verify-git-rules
description: Git 커밋 메시지 및 브랜치 규칙 검증. 작업 내용을 Push 하거나 개발을 완료했을 때 사용.
---

# 커밋 및 브랜치 컨벤션 검증

## Purpose
`git-rules.md`를 바탕으로 프로젝트의 Git 커밋 메시지 컨벤션(Conventional Commits)과 브랜치 전략(main, develop)이 충실하게 적용되었는지 검사합니다.

1. **Branch 보호**: 허용된 브랜치 구조에서 작업 중인지 점검 (1인 체계: `develop` 중심 개발, 배포 시 `main` 머지)
2. **Commit Message 규격**: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `style:` 등 정해진 타입으로 시작하는지 최근 커밋 내역을 검증합니다.

## When to Run
- 코드 작성 후 Git 커밋 시점 혹은 Push 직전
- PR을 올리기 전

## Workflow

### Step 1: 현재 브랜치 구조 점검
터미널을 조작해 현재 위치한 브랜치를 점검합니다.

```bash
current_branch=$(git branch --show-current)
echo "Current Branch: $current_branch"
```
**판단 기준**: `develop` 혹은 `main` 브랜치에 위치해야만 정상(PASS). 기능(feature) 등 별도 브랜치로 분리되었다면 `develop`으로 돌아와 작업할 것을 안내하세요.

### Step 2: 커밋 컨벤션 점검
가장 최근의 커밋 N개를 확인해 Conventional Commits 규격을 따르고 있는지 정규식을 통해 검사합니다.

```bash
# 가장 최근의 커밋 5개를 출력하여 확인합니다.
git log -5 --pretty=format:"%h - %s"
```

터미널에서 가져온 Git 커밋 메시지가 다음의 정규식 구조를 만족하는지 분석하세요.
- 패턴: `^(feat|fix|docs|style|refactor|chore)(\([a-z0-9_\-]+\))?:\s[a-zA-Z0-9가-힣\s]+`
- 예시: `feat: 로그인 화면 분리`, `fix: 자산 가치 계산 오류 수정`

### Step 3: 자동화 스크립트 실행 (Optional)
사용자 환경에서 간단히 복사 실행하여 점검할 수 있는 스크립트를 제공합니다. 필요시 에이전트가 직접 실행하세요.

```bash
# /tmp/verify_commits.sh 에 저장 후 실행
#!/bin/bash
echo "** Branch Validation **"
CURRENT=$(git branch --show-current)
if [[ "$CURRENT" != "main" && "$CURRENT" != "develop" ]]; then
    echo "FAIL: 허용되지 않은 브랜치($CURRENT). 1인 프로젝트 규칙상 'develop'을 사용하세요."
else
    echo "PASS: Branch ($CURRENT)"
fi

echo -e "\n** Commit Message Validation (Last 5 commits) **"
REGEX="^(feat|fix|docs|style|refactor|chore|test)(\([a-z0-9_-]+\))?: .+"
git log -5 --pretty=format:"%s" | while read -r line; do
    if [[ $line =~ $REGEX ]]; then
        echo "PASS: $line"
    elif [[ $line == Merge* ]]; then
        echo "SKIP: $line (Merge commit)"
    else
        echo "FAIL: $line"
    fi
done
```

## Output Format
| 검증 항목 | 진단 결과 | 해결 방안 |
|-----------|-----------|-----------|
| 현재 Branch | PASS / FAIL | (FAIL 시 `git checkout develop` 가이드) |
| 최소 커밋 메시지 규격 | PASS / FAIL / 부분 FAIL | 커밋 수정을 위한 `git commit --amend` 가이드 제공 |
