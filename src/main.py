import os
import json
import requests
import glob
from datetime import datetime, timezone
import pytz
from utils import sanitize_filename

def main():
    github_token = os.environ['INPUT_GITHUB-TOKEN']
    output_dir = os.environ['INPUT_OUTPUT-DIR']
    trigger_label = os.environ['INPUT_TRIGGER-LABEL']
    timezone_name = os.environ['INPUT_TIMEZONE']
    
    with open(os.environ['GITHUB_EVENT_PATH'], 'r') as f:
        event = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if event['action'] == 'labeled' and trigger_label in event['label']['name']:
        add_issue_file(event, output_dir, headers, timezone_name)
    elif event['action'] == 'unlabeled' and trigger_label in event['label']['name']:
        remove_issue_file(event, output_dir, headers, timezone_name)
    elif event['action'] == 'deleted':
        remove_issue_file(event, output_dir, headers, timezone_name)

def add_issue_file(event, output_dir, headers, timezone_name):
    tz = pytz.timezone(timezone_name)
    current_time = datetime.now(timezone.utc).astimezone(tz)
    
    issue = event['issue']
    issue_number = issue['number']
    title = issue['title']
    body = issue['body'] or ''
    
    file_extension = os.environ['INPUT_FILE-EXTENSION'].lstrip('.')
    
    date_str = current_time.strftime('%Y-%m-%d')
    safe_title = sanitize_filename(title)
    filename = f"{output_dir}/{date_str}-issue#{issue_number}-{safe_title}.{file_extension}"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(body)
    
    git_commit(filename, f"sync: Update issue #{issue_number} to file")
    add_comment(event, headers, f"🚀 Sync complete [`{filename}`]")

def remove_issue_file(event, output_dir, headers, timezone_name):
    issue_number = event['issue']['number']
    file_extension = os.environ['INPUT_FILE-EXTENSION'].lstrip('.')
    files = glob.glob(f"{output_dir}/*issue#{issue_number}-*.{file_extension}")
    
    if files:
        for file in files:
            os.remove(file)
            os.system(f'git add "{file}"')
        
        action = "label removed" if event['action'] == 'unlabeled' else "deleted"
        git_commit(None, f"sync: Remove file for {action} issue #{issue_number}")
        
        if event['action'] != 'deleted':
            add_comment(event, headers, f"🗑️ File has been removed - Sync is over")

def add_comment(event, headers, message):
    repo_full_name = event['repository']['full_name']
    issue_number = event['issue']['number']
    
    comments_url = f"https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments"
    comment_data = {"body": message}
    
    requests.post(comments_url, headers=headers, json=comment_data)

def git_commit(file_path, commit_message):
    os.system('git config --global user.name "github-actions[bot]"')
    os.system('git config --global user.email "github-actions[bot]@users.noreply.github.com"')
    os.system('git config --global --add safe.directory /github/workspace')
    
    if file_path:
        os.system(f'git add "{file_path}"')
    else:
        # 삭제된 파일의 경우 모든 변경사항을 스테이징
        os.system('git add -A')
    
    # 변경사항이 있는지 확인
    status = os.popen('git status --porcelain').read().strip()
    if status:
        # 변경사항이 있을 경우에만 커밋 및 푸시
        os.system(f'git commit -m "{commit_message}"')
        os.system('git push')
    else:
        print("No changes to commit")

if __name__ == '__main__':
    main()
