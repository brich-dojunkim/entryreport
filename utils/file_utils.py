import os
from pathlib import Path

def ensure_dir(directory):
    """
    디렉토리가 존재하는지 확인하고 없으면 생성
    
    Parameters:
    - directory: 디렉토리 경로 (문자열 또는 Path 객체)
    
    Returns:
    - 생성된 디렉토리 Path 객체
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_file_extension(file_path):
    """
    파일 확장자 반환
    
    Parameters:
    - file_path: 파일 경로
    
    Returns:
    - 파일 확장자 (소문자)
    """
    return os.path.splitext(file_path)[1].lower()
