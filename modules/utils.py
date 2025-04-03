# modules/utils.py
"""
비플로우 분석 시스템의 유틸리티 함수 모음
"""
import numpy as np
import pandas as pd
import re
import os
from pathlib import Path

def convert_to_serializable(data):
    """
    NumPy 타입과 같은 직렬화 불가능한 데이터를 표준 Python 타입으로 변환
    
    Parameters:
    - data: 변환할 데이터
    
    Returns:
    - 변환된 데이터
    """
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, (np.int64, np.int32, np.int16, np.int8)):
        return int(data)
    elif isinstance(data, (np.float64, np.float32, np.float16)):
        return float(data)
    elif isinstance(data, np.bool_):
        return bool(data)
    elif isinstance(data, np.ndarray):
        return convert_to_serializable(data.tolist())
    elif pd.isna(data):
        return None
    else:
        return data

def safe_process_data(func, *args, default_value=None, error_message="데이터 처리 중 오류", **kwargs):
    """
    안전하게 함수를 실행하고 예외 처리
    
    Parameters:
    - func: 실행할 함수
    - args: 함수에 전달할 위치 인수
    - default_value: 오류 발생시 반환할 기본값
    - error_message: 오류 발생시 출력할 메시지
    - kwargs: 함수에 전달할 키워드 인수
    
    Returns:
    - 함수 실행 결과 또는 오류 발생시 기본값
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"{error_message}: {e}")
        import traceback
        traceback.print_exc()
        return default_value

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

def clean_text(text, stop_words=None):
    """
    텍스트 정제 (불용어 제거, 특수문자 제거 등)
    
    Parameters:
    - text: 정제할 텍스트
    - stop_words: 제거할 불용어 리스트
    
    Returns:
    - 정제된 텍스트
    """
    if not isinstance(text, str):
        return ""
    
    # 소문자 변환
    text = text.lower()
    
    # 불용어 제거
    if stop_words:
        for word in stop_words:
            text = text.replace(word.lower(), ' ')
    
    # 특수문자 제거 (알파벳, 숫자, 한글, 공백만 남김)
    text = re.sub(r'[^\w\s가-힣]', ' ', text)
    
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def format_number(number, decimal_places=1):
    """
    숫자 포맷팅 (천 단위 구분기호, 소수점 자릿수 제한)
    
    Parameters:
    - number: 포맷팅할 숫자
    - decimal_places: 소수점 자릿수
    
    Returns:
    - 포맷팅된 문자열
    """
    if pd.isna(number):
        return "0"
    
    if isinstance(number, (int, float)):
        if number == int(number):
            return format(int(number), ',')
        else:
            return format(round(number, decimal_places), f',.{decimal_places}f')
    
    return str(number)

def extract_keywords(text, min_length=2, max_keywords=10):
    """
    텍스트에서 키워드 추출
    
    Parameters:
    - text: 키워드를 추출할 텍스트
    - min_length: 최소 키워드 길이
    - max_keywords: 최대 추출 키워드 수
    
    Returns:
    - 추출된 키워드 리스트
    """
    if not isinstance(text, str):
        return []
    
    # 한글, 영문 단어 추출
    words = re.findall(r'\b[가-힣a-zA-Z]{%d,}\b' % min_length, text)
    
    # 빈도수 계산
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    
    # 빈도수 기준 정렬 후 상위 키워드 반환
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]

def get_file_extension(file_path):
    """
    파일 확장자 반환
    
    Parameters:
    - file_path: 파일 경로
    
    Returns:
    - 파일 확장자 (소문자)
    """
    return os.path.splitext(file_path)[1].lower()

def is_valid_dataframe(df, required_columns=None):
    """
    데이터프레임의 유효성 검사
    
    Parameters:
    - df: 검사할 데이터프레임
    - required_columns: 필수 컬럼 리스트
    
    Returns:
    - 유효성 여부 (True/False)
    """
    if not isinstance(df, pd.DataFrame):
        return False
    
    if df.empty:
        return False
    
    if required_columns:
        return all(col in df.columns for col in required_columns)
    
    return True