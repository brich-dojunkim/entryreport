# output/report_generator/data_processor/strategy_processor.py
"""
전략/가이드 데이터 처리 모듈
"""
class StrategyProcessor:
    """리포트 전략/가이드 처리 클래스"""
    
    def __init__(self, formatter):
        """
        전략 처리기 초기화
        
        Parameters:
        - formatter: InsightsFormatter 인스턴스
        """
        self.formatter = formatter
    
    def prepare_strategy_variables(self, insights, summary):
        """
        전략 추천 변수 준비 (기존 _prepare_strategy_variables)
        """
        strategy_vars = {}

        guide = self.formatter.get_execution_guide() if self.formatter else None
        if not guide:
            strategy_vars['has_strategy'] = False
            return strategy_vars
        
        strategy_vars['has_strategy'] = True

        # 키워드, 색상 등 예시 추출
        keywords = [kw['name'] for kw in summary.get('top_keywords', [])[:3]]
        colors = [c['name'] for c in summary.get('top_colors', [])[:3]]

        auto_style_keywords = summary.get('auto_style_keywords', [])
        recommended_products = []

        if auto_style_keywords and keywords:
            for i in range(min(3, len(auto_style_keywords), len(keywords))):
                style = auto_style_keywords[i]
                product = keywords[i]
                recommended_products.append(f"{style} {product}")
        else:
            # 예: 다른 방식으로 fall-back
            if len(keywords) > 0:
                recommended_products.append(keywords[0])
        
        strategy_vars['recommended_products'] = recommended_products
        
        # 채널별 상품
        channel_products = {}
        if 'top3_channels' in summary and len(summary['top3_channels']) >= 3:
            ch = summary['top3_channels'][:3]
            # 예: 채널 1 -> [키워드0, 키워드1], 채널 2 -> ...
            if len(keywords) >= 2:
                channel_products[ch[0]] = f"{keywords[0]}/{keywords[1]} 중심"
            else:
                channel_products[ch[0]] = "데이터 부족"
            
        strategy_vars['channel_products'] = channel_products

        # guide에 들어 있는 가격/채널 등 추가 정보
        strategy_vars['main_price_range'] = guide.get('main_price_range', '데이터 없음')
        strategy_vars['main_price_percent'] = guide.get('main_price_percent', 0)
        channels_list = guide.get('channels', [])
        strategy_vars['has_channels'] = len(channels_list) >= 2
        strategy_vars['top_channels'] = ', '.join(channels_list[:2]) if len(channels_list) >= 2 else '데이터 없음'

        # 추가 예: 키워드 추천
        strategy_vars['keyword_recommendations'] = []
        if 'product_keywords' in guide:
            pkeys = guide['product_keywords']
            strategy_vars['keyword_recommendations'].append({
                'name': '상품 키워드',
                'description': ', '.join(pkeys[:3])
            })

        return strategy_vars
