class InsightsFormatter:
    """
    분석 결과(insights)를 보고서와 대시보드에 맞게 포맷팅하는 유틸리티 클래스
    """
    
    @staticmethod
    def get_summary(insights):
        """
        분석 결과에서 요약 정보 추출
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        
        Returns:
        - 요약 정보 딕셔너리
        """
        summary = {}
        
        # 주요 인사이트 추출
        if 'product_keywords' in insights:
            summary['top_keywords'] = insights['product_keywords'].get('top_keywords', [])[:3]
        
        if 'colors' in insights and 'top_items' in insights['colors']:
            summary['top_colors'] = insights['colors'].get('top_items', [])[:3]
        
        if 'price_ranges' in insights:
            price_counts = insights['price_ranges'].get('counts', None)
            if price_counts is not None and not price_counts.empty:
                summary['main_price_range'] = price_counts.idxmax()
                summary['main_price_percent'] = insights['price_ranges'].get('percent', {}).get(summary['main_price_range'], 0)
        
        if 'channels' in insights:
            summary['top3_channels'] = insights['channels'].get('top3_channels', [])
            summary['top3_ratio'] = insights['channels'].get('top3_ratio', 0)
        
        if 'sizes' in insights:
            summary['free_size_ratio'] = insights['sizes'].get('free_size_ratio', 0)
            summary['top_sizes'] = insights['sizes'].get('top_items', [])
        
        # 소재 및 디자인 정보 추출
        if 'materials' in insights and 'top_items' in insights['materials']:
            summary['top_materials'] = [material for material, _ in insights['materials'].get('top_items', [])[:3]]
        
        if 'designs' in insights and 'top_items' in insights['designs']:
            summary['top_designs'] = [design for design, _ in insights['designs'].get('top_items', [])[:3]]
        
        # 베스트셀러 정보
        if 'bestsellers' in insights and 'top_products' in insights['bestsellers']:
            summary['total_orders'] = len(insights['bestsellers'].get('top_products', {}))
            summary['top_products'] = [(product, count) for product, count in 
                                     insights['bestsellers'].get('top_products', {}).items()][:5]
        
        # 자동 추출 키워드 정보 추가
        if 'auto_keywords' in insights:
            if 'style_keywords' in insights['auto_keywords']:
                summary['auto_style_keywords'] = insights['auto_keywords']['style_keywords'][:5]
            
            if 'additional_product_keywords' in insights['auto_keywords']:
                summary['auto_product_keywords'] = [kw for kw, _ in insights['auto_keywords']['additional_product_keywords'][:5]]
                
            if 'color_groups' in insights['auto_keywords']:
                summary['auto_color_groups'] = insights['auto_keywords']['color_groups'][:5]
        
        return summary
    
    @staticmethod
    def generate_insight_text(summary, section):
        """
        각 섹션별 인사이트 텍스트 생성
        
        Parameters:
        - summary: 요약 정보 딕셔너리
        - section: 인사이트 섹션 이름 (product, color, price, channel, size, material_design)
        
        Returns:
        - 인사이트 텍스트
        """
        if section == 'product':
            if not summary.get('top_keywords'):
                return "인기 상품 데이터가 부족합니다."
            
            return (f"{summary['top_keywords'][0][0]}({summary['top_keywords'][0][1]}건), "
                   f"{summary['top_keywords'][1][0]}({summary['top_keywords'][1][1]}건), "
                   f"{summary['top_keywords'][2][0]}({summary['top_keywords'][2][1]}건)이 인기 상품군입니다.")
        
        elif section == 'color':
            if not summary.get('top_colors'):
                return "인기 색상 데이터가 부족합니다."
            
            return (f"{summary['top_colors'][0][0]}({summary['top_colors'][0][1]}건)은 필수 컬러이며, "
                   f"{summary['top_colors'][1][0]}({summary['top_colors'][1][1]}건), "
                   f"{summary['top_colors'][2][0]}({summary['top_colors'][2][1]}건) 순으로 구성하세요.")
        
        elif section == 'price':
            if not summary.get('main_price_range'):
                return "가격대 데이터가 부족합니다."
            
            return (f"{summary['main_price_range']} 상품이 전체의 {summary['main_price_percent']:.1f}%를 "
                   f"차지합니다. 엔트리 셀러는 이 가격대에 집중하세요.")
        
        elif section == 'channel':
            if not summary.get('top3_channels') or len(summary['top3_channels']) < 3:
                return "판매 채널 데이터가 부족합니다."
            
            return (f"{summary['top3_channels'][0]}, {summary['top3_channels'][1]}, {summary['top3_channels'][2]}이 "
                   f"상위 채널로, 이 세 채널에 집중하세요.")
        
        elif section == 'size':
            if 'free_size_ratio' not in summary:
                return "사이즈 데이터가 부족합니다."
            
            size_text = "L, M 사이즈가 그 뒤를 이어 인기 있습니다."
            if 'top_sizes' in summary and len(summary['top_sizes']) > 2:
                # 상위 2개 사이즈(FREE 제외) 추출
                non_free_sizes = [size for size, _ in summary['top_sizes'] if size != 'FREE'][:2]
                if non_free_sizes:
                    size_text = f"{', '.join(non_free_sizes)} 사이즈가 그 뒤를 이어 인기 있습니다."
            
            return (f"FREE 사이즈가 전체의 {summary['free_size_ratio']:.1f}%를 차지합니다. "
                   f"{size_text}")
        
        elif section == 'material_design':
            materials = summary.get('top_materials', [])
            designs = summary.get('top_designs', [])
            
            if not materials or not designs:
                return "소재 및 디자인 데이터가 부족합니다."
            
            materials_str = ', '.join(materials[:2])
            designs_str = ', '.join(designs[:3])
            
            return f"{materials_str} 소재가 인기이며, {designs_str} 디자인이 선호됩니다."
        
        return "데이터 분석 중..."
    
    @staticmethod
    def get_execution_guide(summary, df=None):
        """
        실행 가이드 생성 - 자동 키워드 추출 활용
        
        Parameters:
        - summary: 요약 정보 딕셔너리
        - df: 원본 데이터프레임 (자동 키워드 참조용)
        
        Returns:
        - 실행 가이드 딕셔너리
        """
        # 모든 가이드에 필요한 데이터가 있는지 확인
        if (not summary.get('top_keywords') or 
            not summary.get('top_colors') or 
            not summary.get('main_price_range') or 
            not summary.get('top3_channels')):
            return None
        
        # 추천 상품 구성
        recommended_products = []
        materials = summary.get('top_materials', [])
        designs = summary.get('top_designs', [])
        
        # 인기 키워드 추출
        keywords = [kw for kw, _ in summary.get('top_keywords', [])[:4]]
        
        # 자동 추출 스타일 키워드 사용 (있는 경우)
        auto_style_keywords = summary.get('auto_style_keywords', [])
        
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
        if 'top_products' in summary:
            for product, count in summary['top_products'][:2]:
                short_name = product[:20] + "..." if len(product) > 20 else product
                bestsellers.append(f"{short_name} ({count}건)")
        
        # 키워드 추천 (자동 추출 키워드 추가)
        product_keywords = [kw for kw, _ in summary.get('top_keywords', [])[:4]]
        design_keywords = summary.get('top_designs', [])[:3]
        material_keywords = summary.get('top_materials', [])[:3]
        
        # 자동 추출 키워드 활용
        auto_product_keywords = summary.get('auto_product_keywords', [])
        style_keywords = auto_style_keywords if auto_style_keywords else ["와이드핏", "크롭", "핀턱"]  # 기본값 대신 자동 추출 사용
        
        # 자동 추출 색상 그룹 활용
        color_groups = []
        if 'auto_color_groups' in summary:
            color_groups = [color for color, _ in summary.get('auto_color_groups', [])]
        
        color_keywords = [color for color, _ in summary.get('top_colors', [])[:3]]
        
        # 채널별 추천 상품 생성
        channel_products = {}
        if 'top3_channels' in summary and len(summary['top3_channels']) >= 3:
            channels = summary['top3_channels'][:3]
            
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
            'top_colors': summary.get('top_colors', []),
            'free_size_ratio': summary.get('free_size_ratio', 0),
            'channels': summary.get('top3_channels', []),
            'main_price_range': summary.get('main_price_range', ''),
            'main_price_percent': summary.get('main_price_percent', 0),
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
    
    @staticmethod
    def format_table_data(insights, data_type):
        """
        테이블 형식으로 데이터 포맷팅
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - data_type: 데이터 타입 (keywords, colors, prices, channels, sizes, materials, designs, bestsellers)
        
        Returns:
        - 포맷팅된 데이터 리스트 또는 딕셔너리
        """
        if data_type == 'keywords':
            if 'product_keywords' not in insights or 'top_keywords' not in insights['product_keywords']:
                return []
            return [{"name": k, "value": v} for k, v in insights['product_keywords']['top_keywords'][:10]]
            
        elif data_type == 'colors':
            if 'colors' not in insights or 'top_items' not in insights['colors']:
                return []
            return [{"name": c, "value": v} for c, v in insights['colors']['top_items'][:7]]
            
        elif data_type == 'prices':
            if 'price_ranges' not in insights or 'price_data' not in insights['price_ranges']:
                return []
            return insights['price_ranges']['price_data']
            
        elif data_type == 'channels':
            if 'channels' not in insights or 'channel_data' not in insights['channels']:
                return []
            return insights['channels']['channel_data']
            
        elif data_type == 'sizes':
            if 'sizes' not in insights or 'sizes_data' not in insights['sizes']:
                return []
            return insights['sizes']['sizes_data']
            
        elif data_type == 'materials':
            if 'materials' not in insights or 'materials_data' not in insights['materials']:
                return []
            return insights['materials']['materials_data']
            
        elif data_type == 'designs':
            if 'designs' not in insights or 'designs_data' not in insights['designs']:
                return []
            return insights['designs']['designs_data']
            
        elif data_type == 'bestsellers':
            if 'bestsellers' not in insights or 'bestseller_data' not in insights['bestsellers']:
                return []
            return insights['bestsellers']['bestseller_data']
            
        elif data_type == 'auto_keywords':
            if 'auto_keywords' not in insights:
                return []
            
            # 자동 추출 키워드 데이터 포맷팅
            if 'style_keywords' in insights['auto_keywords']:
                return [{"name": kw, "value": i+1} for i, kw in enumerate(insights['auto_keywords']['style_keywords'][:10])]
            return []
            
        return []