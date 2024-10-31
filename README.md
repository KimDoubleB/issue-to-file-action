# Issue To File Action

A GitHub Action that automatically converts GitHub issues to files using labels.

## Features
- Converts issues with specific labels to files
- Supports custom directory specification
- Timezone setting support
- Automatic cleanup when issues are deleted/labels are removed

## How to Use

1. Create a workflow file (.github/workflows/sync-issues.yml):

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

## Input Parameters

| Parameter | Required | Default | Description |
|----------|------|---------|------|
| github-token | ✅ | - | Github token |
| output-dir | ✅ | - | File save path |
| trigger-label | ✅ | documentation | Sync trigger label |
| timezone | ❌ | Asia/Seoul | Timezone for file name |
| file-extension | ❌ | md | File extension |

## How it Works

- Creates file when specified label is added to an issue
- File naming format: `YYYY-MM-DD-issue#IssueNumber-IssueTitle.extension`
- File is automatically deleted when label is removed or issue is deleted
- Automatically adds a comment to the issue when task is completed
