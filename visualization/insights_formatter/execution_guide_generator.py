# visualization/insights_formatter/execution_guide_generator.py
class ExecutionGuideGenerator:
    """
    요약 정보를 바탕으로 실행 가이드(추천 상품, 채널별 추천 등)를 생성하는 클래스.
    인사이트 데이터는 딕셔너리 리스트 형식으로 가정합니다.
    """
    def __init__(self, summary):
        self.summary = summary

    def generate_guide(self):
        # 필요한 핵심 항목이 없으면 None 반환
        if (not self.summary.get('top_keywords') or 
            not self.summary.get('top_colors') or 
            not self.summary.get('main_price_range') or 
            not self.summary.get('top3_channels')):
            return None
        
        recommended_products = []
        materials = self.summary.get('top_materials', [])
        designs = self.summary.get('top_designs', [])
        # 수정: product_keywords는 이제 딕셔너리 리스트이므로, 각 요소의 'name' 키를 사용
        keywords = [kw['name'] for kw in self.summary.get('top_keywords', [])[:4]]
        auto_style_keywords = self.summary.get('auto_style_keywords', [])
        if auto_style_keywords and keywords:
            for i in range(min(3, len(auto_style_keywords), len(keywords))):
                style = auto_style_keywords[i]
                product = keywords[i]
                recommended_products.append(f"{style} {product}")
        if not recommended_products and materials and designs and keywords:
            # materials, designs는 단순 문자열 리스트로 가정 (SummaryGenerator에서 변환)
            recommended_products.append(f"{designs[0]} {materials[0] if materials else ''} {keywords[0]}")
            if len(keywords) > 1 and len(designs) > 1:
                recommended_products.append(f"{designs[1]} {keywords[1]}")
            if len(keywords) > 2 and len(designs) > 2:
                recommended_products.append(f"{designs[2]} {keywords[2]}")
        
        bestsellers = []
        # bestsellers는 여전히 튜플 리스트(또는 dict 구조)에 따라 처리(출력 모듈에 따라 수정 필요)
        if 'top_products' in self.summary:
            for product, count in self.summary['top_products'][:2]:
                short_name = product[:20] + "..." if len(product) > 20 else product
                bestsellers.append(f"{short_name} ({count}건)")
        
        product_keywords = [kw['name'] for kw in self.summary.get('top_keywords', [])[:4]]
        design_keywords = self.summary.get('top_designs', [])[:3]
        material_keywords = self.summary.get('top_materials', [])[:3]
        auto_product_keywords = self.summary.get('auto_product_keywords', [])
        style_keywords = auto_style_keywords if auto_style_keywords else ["와이드핏", "크롭", "핀턱"]
        
        color_groups = []
        if 'auto_color_groups' in self.summary:
            # auto_color_groups도 딕셔너리 리스트로 가정
            color_groups = [cg['name'] for cg in self.summary.get('auto_color_groups', [])]
        color_keywords = [c['name'] for c in self.summary.get('top_colors', [])[:3]]
        
        channel_products = {}
        if 'top3_channels' in self.summary and len(self.summary['top3_channels']) >= 3:
            channels = self.summary['top3_channels'][:3]
            if product_keywords and len(product_keywords) >= 3:
                channel_products = {
                    channels[0]: f"{product_keywords[0]}/{product_keywords[1]} 중심",
                    channels[1]: f"{product_keywords[1]}/{product_keywords[2]} 위주",
                    channels[2]: f"{design_keywords[0] if design_keywords else ''} {product_keywords[0]}/{product_keywords[2]}"
                }
                if auto_style_keywords and len(auto_style_keywords) >= 2:
                    channel_products[channels[0]] = f"{auto_style_keywords[0]} {product_keywords[0]}/{product_keywords[1]}"
                    if len(channels) > 1 and len(auto_style_keywords) > 1:
                        channel_products[channels[1]] = f"{auto_style_keywords[1]} {product_keywords[1]}/{product_keywords[2]}"
        guide = {
            'recommended_products': recommended_products + bestsellers[:2],
            'top_colors': self.summary.get('top_colors', []),
            'free_size_ratio': self.summary.get('free_size_ratio', 0),
            'channels': self.summary.get('top3_channels', []),
            'main_price_range': self.summary.get('main_price_range', ''),
            'main_price_percent': self.summary.get('main_price_percent', 0),
            'product_keywords': product_keywords,
            'design_keywords': design_keywords,
            'material_keywords': material_keywords,
            'fit_style_keywords': style_keywords,
            'color_keywords': color_keywords,
            'channel_products': channel_products,
            'auto_product_keywords': auto_product_keywords,
            'auto_style_keywords': auto_style_keywords,
            'auto_color_groups': color_groups
        }
        return guide

