# dashboard_generator/data_processor/recommendation_processor.py
"""
추천 데이터 처리 모듈
"""

class RecommendationProcessor:
    """추천 데이터 처리 클래스"""
    
    def __init__(self, formatter):
        """
        추천 처리기 초기화
        
        Parameters:
        - formatter: InsightsFormatter 인스턴스
        """
        self.formatter = formatter
    
    def generate_recommendations(self):
        """
        모든 추천 데이터 생성
        
        Returns:
        - 추천 데이터 딕셔너리
        """
        recommendations = {}
        
        # 실행 가이드 생성
        guide = self.formatter.get_execution_guide()
        
        # 상품 추천
        recommendations['product_recommendations'] = self._generate_product_recommendations(guide)
        
        # 채널 & 가격 전략 추천
        recommendations['channel_recommendations'] = self._generate_channel_recommendations(guide)
        
        # 키워드 추천
        recommendations['keyword_recommendations'] = self._generate_keyword_recommendations(guide)
        
        return recommendations
    
    def _generate_product_recommendations(self, guide):
        """상품 추천 데이터 생성"""
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
        """채널 추천 데이터 생성"""
        channel_recommendations = []
        
        if guide and 'channels' in guide and len(guide['channels']) > 0:
            for i, channel in enumerate(guide['channels'][:3]):
                price_text = f" {guide['main_price_range']}에 집중" if 'main_price_range' in guide else ""
                channel_recommendations.append({
                    'name': f"{channel} 채널",
                    'description': f"진입 중점 채널{price_text}"
                })
                
        if not channel_recommendations:
            channel_recommendations = [{'name': '채널 전략 데이터 없음', 'description': ''}]
            
        return channel_recommendations
    
    def _generate_keyword_recommendations(self, guide):
        """키워드 추천 데이터 생성"""
        keyword_recommendations = []
        
        if guide:
            if 'product_keywords' in guide and len(guide['product_keywords']) > 0:
                keyword_recommendations.append({
                    'name': '상품 키워드',
                    'description': ', '.join(guide['product_keywords'][:3])
                })
                
            if 'color_keywords' in guide and len(guide['color_keywords']) > 0:
                keyword_recommendations.append({
                    'name': '색상',
                    'description': ', '.join(guide['color_keywords'][:3])
                })
                
            if 'material_keywords' in guide and len(guide['material_keywords']) > 0:
                keyword_recommendations.append({
                    'name': '소재',
                    'description': ', '.join(guide['material_keywords'][:3])
                })
                
        if not keyword_recommendations:
            keyword_recommendations = [{'name': '키워드 데이터 없음', 'description': ''}]
            
        return keyword_recommendations