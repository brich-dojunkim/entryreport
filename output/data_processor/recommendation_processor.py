# output/data_processor/recommendation_processor.py
"""
추천(실행 가이드) 데이터 처리 모듈 - 디버깅을 위한 수정
"""
class RecommendationProcessor:
    """추천/가이드 데이터 처리 클래스"""
    
    def __init__(self, formatter):
        self.formatter = formatter
    
    def generate_recommendations(self):
        """
        '마케팅 핵심 키워드' 관련 추천 데이터를 딕셔너리로 반환
        """
        recommendations = {}
        guide = None
        if self.formatter:
            guide = self.formatter.get_execution_guide()
            
        # 디버깅: guide 객체 확인
        print("[디버그] ExecutionGuide 객체: ", guide is not None)
        if guide:
            print("[디버그] Guide 키:", list(guide.keys()))
        
        # 마케팅 키워드 추천만 생성
        keyword_recommendations = self._generate_keyword_recommendations(guide)
        
        # 디버깅: 생성된 키워드 추천 개수 출력
        print(f"[디버그] 생성된 키워드 추천 개수: {len(keyword_recommendations)}")
        for i, rec in enumerate(keyword_recommendations):
            print(f"[디버그] 키워드 {i+1}: {rec.get('name')} - {rec.get('category')}")
        
        recommendations['keyword_recommendations'] = keyword_recommendations
        
        # 이전 항목은 빈 값으로 유지 (호환성)
        recommendations['product_recommendations'] = []
        recommendations['channel_recommendations'] = []
        
        return recommendations
    
    def _generate_keyword_recommendations(self, guide):
        """
        마케팅 키워드 추천 생성 - 카테고리별로 분류하여 제공
        """
        keyword_recommendations = []
        
        if guide:
            # 1. 상품 키워드 (상품명, 태그에 활용)
            if 'product_keywords' in guide and guide['product_keywords']:
                product_kws = guide['product_keywords'][:5]
                print(f"[디버그] 상품 키워드: {product_kws}")
                keyword_recommendations.append({
                    'name': '주력 상품',
                    'description': ', '.join(product_kws),
                    'category': 'product'
                })
                
                # 자동 추출 키워드 추가 - 튜플 형태로 수정
                if 'auto_product_keywords' in guide and guide['auto_product_keywords']:
                    print(f"[디버그] 자동 추출 상품 키워드 타입: {type(guide['auto_product_keywords'])}")
                    print(f"[디버그] 자동 추출 상품 키워드 예시: {guide['auto_product_keywords'][:2]}")
                    
                    # 튜플 또는 딕셔너리 형태에 따라 처리
                    auto_kws = []
                    for item in guide['auto_product_keywords'][:5]:
                        if isinstance(item, tuple) and len(item) >= 1:
                            # 튜플인 경우 첫 번째 요소는 키워드
                            auto_kws.append(item[0])
                        elif isinstance(item, dict) and 'keyword' in item:
                            # 딕셔너리인 경우 'keyword' 키 사용
                            auto_kws.append(item['keyword'])
                        elif isinstance(item, dict) and 'name' in item:
                            # 또는 'name' 키 사용
                            auto_kws.append(item['name'])
                        elif isinstance(item, str):
                            # 문자열인 경우 그대로 사용
                            auto_kws.append(item)
                    
                    if auto_kws:
                        print(f"[디버그] 추출된 자동 상품 키워드: {auto_kws}")
                        keyword_recommendations.append({
                            'name': '연관 상품',
                            'description': ', '.join(auto_kws),
                            'category': 'product'
                        })
            
            # 2. 속성 키워드 (색상, 소재, 디자인)
            # 색상 키워드
            if 'color_keywords' in guide and guide['color_keywords']:
                color_kws = guide['color_keywords'][:5]
                print(f"[디버그] 색상 키워드: {color_kws}")
                keyword_recommendations.append({
                    'name': '인기 색상',
                    'description': ', '.join(color_kws),
                    'category': 'attribute'
                })
            
            # 소재 키워드
            if 'material_keywords' in guide and guide['material_keywords']:
                material_kws = guide['material_keywords'][:5]
                print(f"[디버그] 소재 키워드: {material_kws}")
                keyword_recommendations.append({
                    'name': '주요 소재',
                    'description': ', '.join(material_kws),
                    'category': 'attribute'
                })
                
            # 디자인 키워드
            if 'design_keywords' in guide and guide['design_keywords']:
                design_kws = guide['design_keywords'][:5]
                print(f"[디버그] 디자인 키워드: {design_kws}")
                keyword_recommendations.append({
                    'name': '인기 디자인',
                    'description': ', '.join(design_kws),
                    'category': 'attribute'
                })
            
            # 3. 스타일 키워드 (fit, 트렌드)
            if 'fit_style_keywords' in guide and guide['fit_style_keywords']:
                style_kws = guide['fit_style_keywords'][:5]
                print(f"[디버그] 스타일 키워드: {style_kws}")
                keyword_recommendations.append({
                    'name': '핏 & 스타일',
                    'description': ', '.join(style_kws),
                    'category': 'style'
                })
                
            # 자동 추출 스타일 키워드 - 튜플 또는 딕셔너리 형태에 따라 처리
            if 'auto_style_keywords' in guide and guide['auto_style_keywords']:
                print(f"[디버그] 자동 스타일 키워드 타입: {type(guide['auto_style_keywords'])}")
                print(f"[디버그] 자동 스타일 키워드 샘플: {guide['auto_style_keywords'][:2]}")
                
                auto_style = []
                for item in guide['auto_style_keywords'][:5]:
                    if isinstance(item, dict) and 'name' in item:
                        auto_style.append(item['name'])
                    elif isinstance(item, tuple) and len(item) >= 1:
                        auto_style.append(item[0])
                    elif isinstance(item, str):
                        auto_style.append(item)
                
                if auto_style:
                    print(f"[디버그] 추출된 자동 스타일 키워드: {auto_style}")
                    keyword_recommendations.append({
                        'name': '트렌드 키워드',
                        'description': ', '.join(auto_style),
                        'category': 'style'
                    })
            
            # 4. 프로모션 키워드 (계절, 특별 기획)
            # 현재 월 기반 계절 키워드 생성
            from datetime import datetime
            current_month = datetime.now().month
            
            season_keywords = []
            if 1 <= current_month <= 2 or current_month == 12:
                season_keywords = ["겨울", "방한", "보온", "패딩", "니트"]
            elif 3 <= current_month <= 5:
                season_keywords = ["봄", "경량", "가볍게", "변환", "트렌치"]
            elif 6 <= current_month <= 8:
                season_keywords = ["여름", "시원한", "쿨링", "통풍", "린넨"]
            elif 9 <= current_month <= 11:
                season_keywords = ["가을", "가벼운", "레이어드", "트렌디한", "자켓"]
                
            if season_keywords:
                print(f"[디버그] 계절 키워드({current_month}월): {season_keywords}")
                keyword_recommendations.append({
                    'name': '계절성 키워드',
                    'description': ', '.join(season_keywords),
                    'category': 'promotion'
                })
            
            # 기본 프로모션 키워드 제공
            promo_keywords = ["한정판", "신상품", "베스트셀러", "추천", "인기상품"]
            keyword_recommendations.append({
                'name': '프로모션 키워드',
                'description': ', '.join(promo_keywords),
                'category': 'promotion'
            })
            
            # 주력 상품 카테고리 기반 키워드
            if 'top_categories' in guide and guide['top_categories']:
                top_cats = guide['top_categories'][:2]
                print(f"[디버그] 카테고리 키워드: {top_cats}")
                keyword_recommendations.append({
                    'name': '카테고리 강조',
                    'description': ', '.join(top_cats),
                    'category': 'promotion'
                })
        else:
            print("[디버그] guide 객체가 None입니다!")
            
        return keyword_recommendations