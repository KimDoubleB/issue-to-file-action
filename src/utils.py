import re

def sanitize_filename(filename):
    """파일명에서 사용할 수 없는 문자를 제거하고 안전한 파일명으로 변환"""
    # 공백을 하이픈으로 변경
    filename = filename.lower().replace(' ', '-')
    
    # 파일명에 허용되는 문자만 남기기
    filename = re.sub(r'[^a-z0-9-_]', '', filename)
    
    # 연속된 하이픈을 단일 하이픈으로 변경
    filename = re.sub(r'-+', '-', filename)
    
    # 시작과 끝의 하이픈 제거
    filename = filename.strip('-')
    
    return filename
