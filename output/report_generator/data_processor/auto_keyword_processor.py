# output/report_generator/data_processor/auto_keyword_processor.py
"""
자동 키워드 처리 모듈
"""
class AutoKeywordProcessor:
    """자동 추출 키워드 처리 클래스"""
    
    def prepare_auto_keywords_variables(self, insights):
        """
        자동 추출 키워드 변수 준비
        """
        auto_vars = {}
        
        if 'auto_keywords' not in insights:
            auto_vars['has_auto_keywords'] = False
            return auto_vars
        
        auto_vars['has_auto_keywords'] = True
        auto_keywords = insights['auto_keywords']

        # 1) 스타일 키워드
        style_keywords = auto_keywords.get('style_keywords', [])
        if style_keywords:
            auto_vars['style_keywords'] = style_keywords[:10]
            auto_vars['has_style_keywords'] = True
        else:
            auto_vars['has_style_keywords'] = False

        # 2) 상품 키워드
        product_keywords = auto_keywords.get('additional_product_keywords', [])
        if product_keywords:
            auto_vars['product_keywords'] = [
                {"keyword": kw, "score": float(score)} 
                for kw, score in product_keywords[:8]
            ]
            auto_vars['has_product_keywords'] = True
        else:
            auto_vars['has_product_keywords'] = False

        # 3) 색상 그룹
        raw_color_groups = auto_keywords.get('color_groups', [])
        if raw_color_groups:
            # 튜플 -> 딕셔너리 변환
            color_groups = [
                {'color': c, 'count': float(cnt) if hasattr(cnt, 'item') else cnt}
                for c, cnt in raw_color_groups[:8]
            ]
            auto_vars['color_groups'] = color_groups
            auto_vars['has_color_groups'] = True
        else:
            color_groups = []
            auto_vars['has_color_groups'] = False

        # 4) 인사이트 문장
        auto_insights = []
        
        # (스타일 키워드 인사이트)
        if auto_vars.get('has_style_keywords'):
            top3_styles = style_keywords[:3]
            auto_insights.append({
                'text': f"AI가 분석한 주요 스타일 키워드는 **{', '.join(top3_styles)}**입니다."
            })
            auto_insights.append({
                'text': "이 스타일 키워드를 상품명과 상세 설명에 활용하여 검색 노출을 높일 수 있습니다."
            })

        # (상품 키워드 인사이트)
        if auto_vars.get('has_product_keywords'):
            top3 = [kw['keyword'] for kw in auto_vars['product_keywords'][:3]]
            auto_insights.append({
                'text': f"상품 키워드 분석 결과, **{', '.join(top3)}** 등이 중요하게 나타났습니다."
            })

        # (색상 그룹 인사이트)
        # 반드시 "딕셔너리화한 color_groups"를 사용해야 함
        if auto_vars.get('has_color_groups') and len(color_groups) >= 3:
            c1 = color_groups[0]['color']
            c2 = color_groups[1]['color']
            c3 = color_groups[2]['color']
            auto_insights.append({
                'text': f"색상 그룹 분석 결과, **{c1}**, **{c2}**, **{c3}** 색상군이 두드러집니다."
            })

        auto_vars['auto_insights'] = auto_insights

        return auto_vars
