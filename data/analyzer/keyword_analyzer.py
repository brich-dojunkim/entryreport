# data/analyzer/keyword_analyzer.py
from data.keyword_extractor import KeywordExtractor

def extract_auto_keywords(df, config):
    """
    자동 키워드 추출 함수.
    df와 config를 기반으로 KeywordExtractor를 활용하여 자동 키워드를 추출합니다.
    """
    if df is None or df.empty:
        return {}
    
    try:
        extractor = KeywordExtractor(df, config)
        
        # 스타일 키워드 추출
        style_keywords = extractor.extract_style_keywords(
            column='상품명',
            n_clusters=5,
            n_keywords=3
        )
        # 상품 키워드 추가 추출
        additional_keywords = extractor.extract_product_keywords(
            column='상품명',
            n_keywords=15
        )
        # 색상 그룹 추출
        color_groups = extractor.extract_color_groups()
        
        result = {
            'style_keywords': style_keywords,
            'additional_product_keywords': additional_keywords,
            'color_groups': color_groups
        }
        
        # 디버깅용 출력
        print("[디버그] 자동 키워드 추출 결과:")
        print("style_keywords:", style_keywords)
        print("additional_product_keywords:", additional_keywords)
        print("color_groups:", color_groups)
        
        return result
    except Exception as e:
        print(f"자동 키워드 추출 중 오류 발생: {e}")
        return {}
