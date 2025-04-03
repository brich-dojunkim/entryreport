class InsightsFormatter:
    """
    분석 결과(insights)를 보고서와 대시보드에 맞게 포맷팅하는 클래스
    """
    
    def __init__(self, insights):
        """
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        """
        self.insights = insights
        self.summary = self.get_summary()
    
    def get_summary(self):
        """
        분석 결과에서 요약 정보 추출
        
        Returns:
        - 요약 정보 딕셔너리
        """
        summary = {}
        
        # 주요 인사이트 추출
        if 'product_keywords' in self.insights:
            summary['top_keywords'] = self.insights['product_keywords'].get('top_keywords', [])[:3]
        
        if 'colors' in self.insights and 'top_items' in self.insights['colors']:
            summary['top_colors'] = self.insights['colors'].get('top_items', [])[:3]
        
        if 'price_ranges' in self.insights:
            price_counts = self.insights['price_ranges'].get('counts', None)
            if price_counts is not None and not price_counts.empty:
                summary['main_price_range'] = price_counts.idxmax()
                summary['main_price_percent'] = self.insights['price_ranges'].get('percent', {}).get(summary['main_price_range'], 0)
        
        if 'channels' in self.insights:
            summary['top3_channels'] = self.insights['channels'].get('top3_channels', [])
            summary['top3_ratio'] = self.insights['channels'].get('top3_ratio', 0)
        
        if 'sizes' in self.insights:
            summary['free_size_ratio'] = self.insights['sizes'].get('free_size_ratio', 0)
            summary['top_sizes'] = self.insights['sizes'].get('top_items', [])
        
        # 소재 및 디자인 정보 추출
        if 'materials' in self.insights and 'top_items' in self.insights['materials']:
            summary['top_materials'] = [material for material, _ in self.insights['materials'].get('top_items', [])[:3]]
        
        if 'designs' in self.insights and 'top_items' in self.insights['designs']:
            summary['top_designs'] = [design for design, _ in self.insights['designs'].get('top_items', [])[:3]]
        
        # 베스트셀러 정보
        if 'bestsellers' in self.insights and 'top_products' in self.insights['bestsellers']:
            summary['total_orders'] = len(self.insights['bestsellers'].get('top_products', {}))
            summary['top_products'] = [(product, count) for product, count in 
                                     self.insights['bestsellers'].get('top_products', {}).items()][:5]
        
        # 자동 추출 키워드 정보 추가
        if 'auto_keywords' in self.insights:
            if 'style_keywords' in self.insights['auto_keywords']:
                summary['auto_style_keywords'] = self.insights['auto_keywords']['style_keywords'][:5]
            
            if 'additional_product_keywords' in self.insights['auto_keywords']:
                summary['auto_product_keywords'] = [kw for kw, _ in self.insights['auto_keywords']['additional_product_keywords'][:5]]
                
            if 'color_groups' in self.insights['auto_keywords']:
                summary['auto_color_groups'] = self.insights['auto_keywords']['color_groups'][:5]
        
        return summary
    
    def generate_insight_text(self, section):
        """
        각 섹션별 인사이트 텍스트 생성
        
        Parameters:
        - section: 인사이트 섹션 이름 (product, color, price, channel, size, material_design)
        
        Returns:
        - 인사이트 텍스트
        """
        if section == 'product':
            if not self.summary.get('top_keywords'):
                return "인기 상품 데이터가 부족합니다."
            
            return (f"{self.summary['top_keywords'][0][0]}({self.summary['top_keywords'][0][1]}건), "
                   f"{self.summary['top_keywords'][1][0]}({self.summary['top_keywords'][1][1]}건), "
                   f"{self.summary['top_keywords'][2][0]}({self.summary['top_keywords'][2][1]}건)이 인기 상품군입니다.")
        
        elif section == 'color':
            if not self.summary.get('top_colors'):
                return "인기 색상 데이터가 부족합니다."
            
            return (f"{self.summary['top_colors'][0][0]}({self.summary['top_colors'][0][1]}건)은 필수 컬러이며, "
                   f"{self.summary['top_colors'][1][0]}({self.summary['top_colors'][1][1]}건), "
                   f"{self.summary['top_colors'][2][0]}({self.summary['top_colors'][2][1]}건) 순으로 구성하세요.")
        
        elif section == 'price':
            if not self.summary.get('main_price_range'):
                return "가격대 데이터가 부족합니다."
            
            return (f"{self.summary['main_price_range']} 상품이 전체의 {self.summary['main_price_percent']:.1f}%를 "
                   f"차지합니다. 엔트리 셀러는 이 가격대에 집중하세요.")
        
        elif section == 'channel':
            if not self.summary.get('top3_channels') or len(self.summary['top3_channels']) < 3:
                return "판매 채널 데이터가 부족합니다."
            
            return (f"{self.summary['top3_channels'][0]}, {self.summary['top3_channels'][1]}, {self.summary['top3_channels'][2]}이 "
                   f"상위 채널로, 이 세 채널에 집중하세요.")
        
        elif section == 'size':
            if 'free_size_ratio' not in self.summary:
                return "사이즈 데이터가 부족합니다."
            
            size_text = "L, M 사이즈가 그 뒤를 이어 인기 있습니다."
            if 'top_sizes' in self.summary and len(self.summary['top_sizes']) > 2:
                # 상위 2개 사이즈(FREE 제외) 추출
                non_free_sizes = [size for size, _ in self.summary['top_sizes'] if size != 'FREE'][:2]
                if non_free_sizes:
                    size_text = f"{', '.join(non_free_sizes)} 사이즈가 그 뒤를 이어 인기 있습니다."
            
            return (f"FREE 사이즈가 전체의 {self.summary['free_size_ratio']:.1f}%를 차지합니다. "
                   f"{size_text}")
        
        elif section == 'material_design':
            materials = self.summary.get('top_materials', [])
            designs = self.summary.get('top_designs', [])
            
            if not materials or not designs:
                return "소재 및 디자인 데이터가 부족합니다."
            
            materials_str = ', '.join(materials[:2])
            designs_str = ', '.join(designs[:3])
            
            return f"{materials_str} 소재가 인기이며, {designs_str} 디자인이 선호됩니다."
        
        return "데이터 분석 중..."
    
    def get_execution_guide(self, df=None):
        """
        실행 가이드 생성 - 자동 키워드 추출 활용
        
        Parameters:
        - df: 원본 데이터프레임 (자동 키워드 참조용)
        
        Returns:
        - 실행 가이드 딕셔너리
        """
        # 모든 가이드에 필요한 데이터가 있는지 확인
        if (not self.summary.get('top_keywords') or 
            not self.summary.get('top_colors') or 
            not self.summary.get('main_price_range') or 
            not self.summary.get('top3_channels')):
            return None
        
        # 추천 상품 구성
        recommended_products = []
        materials = self.summary.get('top_materials', [])
        designs = self.summary.get('top_designs', [])
        
        # 인기 키워드 추출
        keywords = [kw for kw, _ in self.summary.get('top_keywords', [])[:4]]
        
        # 자동 추출 스타일 키워드 사용 (있는 경우)
        auto_style_keywords = self.summary.get('auto_style_keywords', [])
        
        # 자동 스타일 키워드를 활용한 상품 추천
        if auto_style_keywords and keywords:
            for i in range(min(3, len(auto_style_keywords), len(keywords))):
                style = auto_style_keywords[i]
                product = keywords[i if i < len(keywords) else 0]
                recommended_products.append(f"{style} {product}")
        
        # 기존 방식의 상품 조합 추천 (자동 키워드가 없거나 부족한 경우)
        if not recommended_products and materials and designs and keywords:
            # 디자인 + 소재 + 상품유형 조합 생성
            recommended_products.append(f"{designs[0]} {materials[0] if materials else ''} {keywords[0]}")
            if len(keywords) > 1 and len(designs) > 1:
                recommended_products.append(f"{designs[1]} {keywords[1]}")
            if len(keywords) > 2 and len(designs) > 2:
                recommended_products.append(f"{designs[2]} {keywords[2]}")
        
        # 베스트셀러가 있으면 추가
        bestsellers = []
        if 'top_products' in self.summary:
            for product, count in self.summary['top_products'][:2]:
                short_name = product[:20] + "..." if len(product) > 20 else product
                bestsellers.append(f"{short_name} ({count}건)")
        
        # 키워드 추천 (자동 추출 키워드 추가)
        product_keywords = [kw for kw, _ in self.summary.get('top_keywords', [])[:4]]
        design_keywords = self.summary.get('top_designs', [])[:3]
        material_keywords = self.summary.get('top_materials', [])[:3]
        
        # 자동 추출 키워드 활용
        auto_product_keywords = self.summary.get('auto_product_keywords', [])
        style_keywords = auto_style_keywords if auto_style_keywords else ["와이드핏", "크롭", "핀턱"]  # 기본값 대신 자동 추출 사용
        
        # 자동 추출 색상 그룹 활용
        color_groups = []
        if 'auto_color_groups' in self.summary:
            color_groups = [color for color, _ in self.summary.get('auto_color_groups', [])]
        
        color_keywords = [color for color, _ in self.summary.get('top_colors', [])[:3]]
        
        # 채널별 추천 상품 생성
        channel_products = {}
        if 'top3_channels' in self.summary and len(self.summary['top3_channels']) >= 3:
            channels = self.summary['top3_channels'][:3]
            
            # 각 채널별 추천 상품 매핑 (자동 추출 키워드 활용)
            if product_keywords and len(product_keywords) >= 3:
                channel_products = {
                    channels[0]: f"{product_keywords[0]}/{product_keywords[1]} 중심",
                    channels[1]: f"{product_keywords[1]}/{product_keywords[2]} 위주",
                    channels[2]: f"{design_keywords[0] if design_keywords else ''} {product_keywords[0]}/{product_keywords[2]}"
                }
                
                # 자동 추출 스타일 키워드가 있으면 활용
                if auto_style_keywords and len(auto_style_keywords) >= 2:
                    channel_products[channels[0]] = f"{auto_style_keywords[0]} {product_keywords[0]}/{product_keywords[1]}"
                    
                    if len(channels) > 1 and len(auto_style_keywords) > 1:
                        channel_products[channels[1]] = f"{auto_style_keywords[1]} {product_keywords[1]}/{product_keywords[2]}"
        
        # 가이드 데이터 생성
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
    
    def format_table_data(self, data_type):
        """
        테이블 형식으로 데이터 포맷팅
        
        Parameters:
        - data_type: 데이터 타입 (keywords, colors, prices, channels, sizes, materials, designs, bestsellers)
        
        Returns:
        - 포맷팅된 데이터 리스트 또는 딕셔너리
        """
        if data_type == 'keywords':
            if 'product_keywords' not in self.insights or 'top_keywords' not in self.insights['product_keywords']:
                return []
            return [{"name": k, "value": v} for k, v in self.insights['product_keywords']['top_keywords'][:10]]
            
        elif data_type == 'colors':
            if 'colors' not in self.insights or 'top_items' not in self.insights['colors']:
                return []
            return [{"name": c, "value": v} for c, v in self.insights['colors']['top_items'][:7]]
            
        elif data_type == 'prices':
            if 'price_ranges' not in self.insights or 'price_data' not in self.insights['price_ranges']:
                return []
            return self.insights['price_ranges']['price_data']
            
        elif data_type == 'channels':
            if 'channels' not in self.insights or 'channel_data' not in self.insights['channels']:
                return []
            return self.insights['channels']['channel_data']
            
        elif data_type == 'sizes':
            if 'sizes' not in self.insights or 'sizes_data' not in self.insights['sizes']:
                return []
            return self.insights['sizes']['sizes_data']
            
        elif data_type == 'materials':
            if 'materials' not in self.insights or 'materials_data' not in self.insights['materials']:
                return []
            return self.insights['materials']['materials_data']
            
        elif data_type == 'designs':
            if 'designs' not in self.insights or 'designs_data' not in self.insights['designs']:
                return []
            return self.insights['designs']['designs_data']
            
        elif data_type == 'bestsellers':
            if 'bestsellers' not in self.insights or 'bestseller_data' not in self.insights['bestsellers']:
                return []
            return self.insights['bestsellers']['bestseller_data']
            
        elif data_type == 'auto_keywords':
            if 'auto_keywords' not in self.insights:
                return []
            
            # 자동 추출 키워드 데이터 포맷팅
            if 'style_keywords' in self.insights['auto_keywords']:
                return [{"name": kw, "value": i+1} for i, kw in enumerate(self.insights['auto_keywords']['style_keywords'][:10])]
            return []
            
        return []