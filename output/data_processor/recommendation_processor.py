# output/data_processor/recommendation_processor.py
"""
추천(실행 가이드) 데이터 처리 모듈
"""
class RecommendationProcessor:
    """추천/가이드 데이터 처리 클래스"""
    
    def __init__(self, formatter):
        self.formatter = formatter
    
    def generate_recommendations(self):
        """
        '실행 가이드' 관련 추천 데이터(상품·채널·키워드)를 딕셔너리로 반환
        """
        recommendations = {}
        guide = None
        if self.formatter:
            guide = self.formatter.get_execution_guide()
        
        # 상품 추천
        recommendations['product_recommendations'] = self._generate_product_recommendations(guide)
        
        # 채널 & 가격 전략
        recommendations['channel_recommendations'] = self._generate_channel_recommendations(guide)
        
        # 키워드 추천
        recommendations['keyword_recommendations'] = self._generate_keyword_recommendations(guide)
        
        return recommendations
    
    def _generate_product_recommendations(self, guide):
        product_recommendations = []
        
        if guide and 'recommended_products' in guide:
            for i, product in enumerate(guide['recommended_products'][:3]):
                product_recommendations.append({
                    'name': f"{i+1}. {product}" if isinstance(product, str) else f"{i+1}. 추천 상품",
                    'description': "인기 키워드 및 색상 조합"
                })
        
        if not product_recommendations:
            product_recommendations = [{'name': '추천 상품 데이터 없음', 'description': ''}]
            
        return product_recommendations
    
    def _generate_channel_recommendations(self, guide):
        channel_recommendations = []
        
        if guide and 'channels' in guide and guide['channels']:
            for i, channel in enumerate(guide['channels'][:3]):
                price_text = ""
                if 'main_price_range' in guide:
                    price_text = f" {guide['main_price_range']}에 집중"
                channel_recommendations.append({
                    'name': f"{channel} 채널",
                    'description': f"진입 중점 채널{price_text}"
                })
        
        if not channel_recommendations:
            channel_recommendations = [{'name': '채널 전략 데이터 없음', 'description': ''}]
            
        return channel_recommendations
    
    def _generate_keyword_recommendations(self, guide):
        keyword_recommendations = []
        
        if guide:
            if 'product_keywords' in guide and guide['product_keywords']:
                keyword_recommendations.append({
                    'name': '상품 키워드',
                    'description': ', '.join(guide['product_keywords'][:3])
                })
            
            if 'color_keywords' in guide and guide['color_keywords']:
                keyword_recommendations.append({
                    'name': '색상',
                    'description': ', '.join(guide['color_keywords'][:3])
                })
            
            if 'material_keywords' in guide and guide['material_keywords']:
                keyword_recommendations.append({
                    'name': '소재',
                    'description': ', '.join(guide['material_keywords'][:3])
                })
        
        if not keyword_recommendations:
            keyword_recommendations = [{'name': '키워드 데이터 없음', 'description': ''}]
            
        return keyword_recommendations
