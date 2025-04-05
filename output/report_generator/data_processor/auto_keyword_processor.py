# output/data_processor/auto_keyword_processor.py
"""
자동 키워드 처리 모듈
"""
class AutoKeywordProcessor:
    """자동 추출 키워드 (스타일/상품/색상) 처리 클래스"""
    
    def prepare_auto_keywords_variables(self, insights):
        auto_vars = {}

        if 'auto_keywords' not in insights:
            auto_vars['has_auto_keywords'] = False
            return auto_vars
        
        auto_vars['has_auto_keywords'] = True
        auto_keywords = insights['auto_keywords']

        # (1) 스타일 키워드
        style_keywords = auto_keywords.get('style_keywords', [])
        if style_keywords:
            auto_vars['style_keywords'] = style_keywords[:10]
            auto_vars['has_style_keywords'] = True
        else:
            auto_vars['has_style_keywords'] = False

        # (2) 상품 키워드
        product_keywords = auto_keywords.get('additional_product_keywords', [])
        if product_keywords:
            auto_vars['product_keywords'] = [
                {"keyword": kw, "score": float(score)} for kw, score in product_keywords[:8]
            ]
            auto_vars['has_product_keywords'] = True
        else:
            auto_vars['has_product_keywords'] = False

        # (3) 색상 그룹
        raw_color_groups = auto_keywords.get('color_groups', [])
        if raw_color_groups:
            color_groups = [
                {'color': c, 'count': float(cnt)}
                for c, cnt in raw_color_groups[:8]
            ]
            auto_vars['color_groups'] = color_groups
            auto_vars['has_color_groups'] = True
        else:
            auto_vars['has_color_groups'] = False

        # (4) 자동 인사이트 문장
        auto_insights = []
        if auto_vars.get('has_style_keywords'):
            top3_styles = style_keywords[:3]
            auto_insights.append({
                'text': f"주요 스타일 키워드는 {', '.join(top3_styles)} 입니다."
            })
        if auto_vars.get('has_product_keywords'):
            top3 = [kw['keyword'] for kw in auto_vars['product_keywords'][:3]]
            auto_insights.append({
                'text': f"상품 키워드 상위 3개는 {', '.join(top3)} 입니다."
            })
        if auto_vars.get('has_color_groups'):
            cg = auto_vars['color_groups']
            c_names = [c['color'] for c in cg[:3]]
            auto_insights.append({
                'text': f"주요 색상은 {', '.join(c_names)} 입니다."
            })
        auto_vars['auto_insights'] = auto_insights

        return auto_vars
