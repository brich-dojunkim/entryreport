import pandas as pd

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
