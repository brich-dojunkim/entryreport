import re

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
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # 빈도수 기준 정렬 후 상위 키워드 반환
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]
