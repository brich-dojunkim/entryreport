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
    
    # 카테고리 계층 분석
    depth_analysis = {}
    for cat in top_categories.index:
        # 숫자형이면 문자열로 변환
        if isinstance(cat, (int, float)):
            cat_str = str(int(cat))
        else:
            cat_str = str(cat)
        
        if len(cat_str) >= 4:  # Depth 1
            depth1 = cat_str[:4]
            if depth1 not in depth_analysis:
                depth_analysis[depth1] = {
                    'name': config.get_category_name(depth1),
                    'total_count': 0,
                    'subcategories': {}
                }
            
            depth_analysis[depth1]['total_count'] += top_categories[cat]
            
            # Depth 2 분석
            if len(cat_str) >= 8:
                depth2 = cat_str[:8]
                if depth2 not in depth_analysis[depth1]['subcategories']:
                    depth_analysis[depth1]['subcategories'][depth2] = {
                        'name': config.get_category_name(depth2),
                        'count': 0
                    }
                depth_analysis[depth1]['subcategories'][depth2]['count'] += top_categories[cat]
    
    # 카테고리 매핑 적용
    category_mapping = {}
    for cat in top_categories.index:
        category_mapping[cat] = config.get_category_name(cat)
        
    return {
        'counts': category_counts,
        'top_categories': top_categories,
        'mapping': category_mapping,
        'depth_analysis': depth_analysis,
        'category_data': [
            {
                'name': config.get_category_name(cat),
                'id': cat,
                'value': count
            }
            for cat, count in top_categories.items()
        ]
    }