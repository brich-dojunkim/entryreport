# utils/data_conversion.py
import numpy as np
import pandas as pd

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
        # 디버깅: 딕셔너리 변환 과정 추적
        converted_dict = {}
        for key, value in data.items():
            # 'category' 키 보존 확인
            if key == 'category':
                print(f"[변환-디버그] 'category' 키 발견: {value}")
            converted_dict[key] = convert_to_serializable(value)
        return converted_dict
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