# output/report_generator/data_processor/auto_keyword_processor.py
"""
자동 키워드 처리 모듈
"""
class AutoKeywordProcessor:
    """자동 추출 키워드 처리 클래스"""
    
    def prepare_auto_keywords_variables(self, insights):
        """
        자동 추출 키워드 변수 준비 (기존 _prepare_auto_keywords_variables)
        """
        auto_vars = {}
        
        if 'auto_keywords' not in insights:
            auto_vars['has_auto_keywords'] = False
            return auto_vars
        
        auto_vars['has_auto_keywords'] = True
        auto_keywords = insights['auto_keywords']

        # 스타일 키워드
        style_keywords = auto_keywords.get('style_keywords', [])
        if style_keywords:
            auto_vars['style_keywords'] = style_keywords[:10]
            auto_vars['has_style_keywords'] = True
        else:
            auto_vars['has_style_keywords'] = False

        # 상품 키워드
        product_keywords = auto_keywords.get('additional_product_keywords', [])
        if product_keywords:
            auto_vars['product_keywords'] = [
                {"keyword": kw, "score": float(score)} for kw, score in product_keywords[:8]
            ]
            auto_vars['auto_product_keywords'] = [kw for kw, _ in product_keywords[:8]]
            auto_vars['has_product_keywords'] = True
        else:
            auto_vars['has_product_keywords'] = False

        # 색상 그룹
        color_groups = auto_keywords.get('color_groups', [])
        if color_groups:
            auto_vars['color_groups'] = [
                {'color': c, 'count': float(cnt) if hasattr(cnt, 'item') else cnt}
                for c, cnt in color_groups[:8]
            ]
            auto_vars['has_color_groups'] = True
        else:
            auto_vars['has_color_groups'] = False

        # 간단한 인사이트 텍스트
        auto_insights = []
        if auto_vars.get('has_style_keywords', False):
            top3_styles = style_keywords[:3]
            auto_insights.append({
                'text': f"AI가 분석한 주요 스타일 키워드는 **{', '.join(top3_styles)}**입니다."
            })
            auto_insights.append({
                'text': "이 스타일 키워드를 상품명과 상세 설명에 활용하여 검색 노출을 높일 수 있습니다."
            })

        if auto_vars.get('has_product_keywords', False):
            top3 = [kw for kw, _ in product_keywords[:3]]
            auto_insights.append({
                'text': f"상품 키워드 분석 결과, **{', '.join(top3)}** 등이 중요하게 나타났습니다."
            })

        if auto_vars.get('has_color_groups', False) and len(color_groups) >= 3:
            c1, c2, c3 = color_groups[0][0], color_groups[1][0], color_groups[2][0]
            auto_insights.append({
                'text': f"색상 그룹 분석 결과, **{c1}**, **{c2}**, **{c3}** 색상군을 중심으로 구성하는 것이 효과적입니다."
            })

        auto_vars['auto_insights'] = auto_insights

        return auto_vars
