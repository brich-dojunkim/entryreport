# output/data_processor/strategy_processor.py
"""
전략/가이드 데이터 처리 모듈
"""
class StrategyProcessor:
    """리포트 전략/가이드 처리 클래스"""
    
    def __init__(self, formatter):
        self.formatter = formatter
    
    def prepare_strategy_variables(self, insights, summary):
        """
        전략 관련 변수 (has_strategy, recommended_products, main_price_range 등)를 구성
        """
        strategy_vars = {}
        guide = None
        if self.formatter:
            guide = self.formatter.get_execution_guide()
        
        if not guide:
            strategy_vars['has_strategy'] = False
            return strategy_vars
        
        strategy_vars['has_strategy'] = True
        strategy_vars['recommended_products'] = guide.get('recommended_products', [])
        strategy_vars['main_price_range'] = guide.get('main_price_range', '정보 없음')
        strategy_vars['main_price_percent'] = guide.get('main_price_percent', 0)
        
        channels_list = guide.get('channels', [])
        strategy_vars['has_channels'] = bool(channels_list)
        strategy_vars['top_channels'] = ', '.join(channels_list[:2]) if channels_list else '채널 없음'
        
        # 추가 키워드
        strategy_vars['keyword_recommendations'] = guide.get('product_keywords', [])
        
        return strategy_vars
