# data/analyzer/utils.py

def format_items(items):
    """
    리스트 형식의 (이름, 개수) 튜플을 차트용 포맷(딕셔너리 리스트)으로 변환합니다.
    """
    formatted = []
    for name, count in items:
        formatted.append({'name': name, 'count': count, 'value': count})
    return formatted
