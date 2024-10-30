# Issue To File Action

GitHub 이슈를 파일로 자동 변환하는 GitHub Action입니다.

## 특징

- 특정 라벨이 지정된 이슈를 파일로 변환
- 커스텀 디렉토리 지정 가능
- 타임존 설정 지원
- 이슈 삭제/라벨 제거 시 자동 정리

## 사용 방법

1. 워크플로우 파일 생성 (.github/workflows/sync-issues.yml):

```yaml
name: Sync Issues to File

on:
  issues:
    types: [labeled, unlabeled, deleted]

jobs:
  sync-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Sync Issue to File
        uses: KimDoubleB/issue-to-file-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output-dir: 'content/issues'
          trigger-label: 'documentation'
          timezone: 'Asia/Seoul'
          file-extension: 'md'
```

## 입력 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|----------|------|---------|------|
| github-token | ✅ | - | GitHub 토큰 |
| output-dir | ✅ | - | 마크다운 파일 저장 경로 |
| trigger-label | ✅ | documentation | 변환 트리거 라벨 |
| timezone | ❌ | Asia/Seoul | 날짜/시간 타임존 |
| file-extension | ❌ | md | 파일 확장자 |

## 동작 방식

1. 이슈에 지정된 라벨이 추가되면 마크다운 파일 생성
2. 파일명 형식: `YYYY-MM-DD-issue#이슈번호-이슈제목.확장자`
3. 라벨이 제거되거나 이슈가 삭제되면 파일도 자동 삭제
4. 작업 완료시 이슈에 자동으로 코멘트 추가

## 라이선스

MIT
