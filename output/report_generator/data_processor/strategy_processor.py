# output/report_generator/data_processor/strategy_processor.py
"""
전략/가이드 데이터 처리 모듈 (간소화 버전)
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
        전략 추천 변수 준비
        """
        strategy_vars = {}

        # formatter에서 실행 가이드를 받아온다고 가정
        guide = self.formatter.get_execution_guide() if self.formatter else None
        if not guide:
            strategy_vars['has_strategy'] = False
            return strategy_vars
        
        strategy_vars['has_strategy'] = True

        # 키워드, 색상 등 간단 예시 추출
        keywords = [kw['name'] for kw in summary.get('top_keywords', [])[:3]]
        colors = [c['name'] for c in summary.get('top_colors', [])[:3]]
        
        # 추천 상품
        recommended_products = []
        # 예: 자동 스타일 키워드 vs 실제 상위 키워드 결합
        auto_style_keywords = summary.get('auto_style_keywords', [])
        if auto_style_keywords and keywords:
            for i in range(min(len(auto_style_keywords), len(keywords), 3)):
                recommended_products.append(f"{auto_style_keywords[i]} {keywords[i]}")
        elif keywords:
            recommended_products.append(keywords[0])

        strategy_vars['recommended_products'] = recommended_products
        
        # 예: 채널/가격 가이드
        strategy_vars['main_price_range'] = guide.get('main_price_range', '정보 없음')
        strategy_vars['main_price_percent'] = guide.get('main_price_percent', 0)
        channels_list = guide.get('channels', [])
        strategy_vars['has_channels'] = len(channels_list) >= 1
        strategy_vars['top_channels'] = ', '.join(channels_list[:2]) if channels_list else '채널 데이터 없음'
        
        # 추가 키워드 추천
        strategy_vars['keyword_recommendations'] = guide.get('product_keywords', [])
        
        return strategy_vars
