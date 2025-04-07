# data/analyzer/category_analyzer.py
import pandas as pd

def analyze_categories(df, config):
    """
    카테고리 분석 함수.
    df의 '상품 카테고리' 컬럼을 분석하고, 카테고리 매핑 정보를 포함한 결과를 반환합니다.
    """
    if '상품 카테고리' not in df.columns:
        return {
            'counts': pd.Series(dtype=int),
            'top_categories': pd.Series(dtype=int)
        }
    
    category_counts = df['상품 카테고리'].value_counts()
    top_categories = category_counts.head(10)
    
    category_mapping = {}
    for cat in top_categories.index:
        category_mapping[cat] = config.get_category_name(cat)
        
    return {
        'counts': category_counts,
        'top_categories': top_categories,
        'mapping': category_mapping,
        'category_data': [
            {
                'name': config.get_category_name(cat),
                'id': cat,
                'value': count
            }
            for cat, count in top_categories.items()
        ]
    }
