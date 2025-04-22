class InsightTextGenerator:
    """
    요약 정보를 기반으로 섹션별 인사이트 텍스트를 생성하는 클래스.
    반환된 summary의 각 항목은 딕셔너리 리스트 형태임을 전제로 합니다.
    """
    def __init__(self, summary):
        self.summary = summary

    def generate_text(self, section):
        if section == 'product':
            if not self.summary.get('top_keywords') or len(self.summary['top_keywords']) < 3:
                return "인기 상품 데이터가 부족합니다."
            return (f"{self.summary['top_keywords'][0]['name']}({self.summary['top_keywords'][0]['count']}건), "
                    f"{self.summary['top_keywords'][1]['name']}({self.summary['top_keywords'][1]['count']}건), "
                    f"{self.summary['top_keywords'][2]['name']}({self.summary['top_keywords'][2]['count']}건)이 인기 상품군입니다.")
        elif section == 'color':
            if not self.summary.get('top_colors') or len(self.summary['top_colors']) < 3:
                return "인기 색상 데이터가 부족합니다."
            return (f"{self.summary['top_colors'][0]['name']}({self.summary['top_colors'][0]['count']}건)은 필수 컬러이며, "
                    f"{self.summary['top_colors'][1]['name']}({self.summary['top_colors'][1]['count']}건), "
                    f"{self.summary['top_colors'][2]['name']}({self.summary['top_colors'][2]['count']}건) 순으로 구성하세요.")
        elif section == 'price':
            if not self.summary.get('main_price_range'):
                return "가격대 데이터가 부족합니다."
            return (f"{self.summary['main_price_range']} 상품이 전체의 {self.summary['main_price_percent']:.1f}%를 "
                    f"차지합니다. 엔트리 셀러는 이 가격대에 집중하세요.")
        elif section == 'channel':
            if not self.summary.get('top3_channels') or len(self.summary['top3_channels']) < 3:
                return "판매 채널 데이터가 부족합니다."
            return (f"{', '.join(self.summary['top3_channels'])}이 상위 채널로, 이 세 채널에 집중하세요.")
        elif section == 'size':
            if 'free_size_ratio' not in self.summary or 'top_sizes' not in self.summary:
                return "사이즈 데이터가 부족합니다."
            size_text = "L, M 사이즈가 그 뒤를 이어 인기 있습니다."
            non_free_sizes = [item['name'] for item in self.summary['top_sizes'] if item['name'] != 'FREE']
            if non_free_sizes:
                size_text = f"{', '.join(non_free_sizes[:2])} 사이즈가 그 뒤를 이어 인기 있습니다."
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
        elif section == 'material':
            materials = self.summary.get('top_materials', [])
            if not materials:
                return "소재 데이터가 부족합니다."
            materials_str = ', '.join(materials[:3])
            return f"{materials_str} 등의 소재가 주로 사용되고 있습니다."
        elif section == 'design':
            designs = self.summary.get('top_designs', [])
            if not designs:
                return "디자인 데이터가 부족합니다."
            designs_str = ', '.join(designs[:3])
            return f"{designs_str} 등의 디자인 요소가 트렌드를 이끌고 있습니다."
        elif section == 'bestseller':
            if not self.summary.get('top_products') or len(self.summary.get('top_products', [])) < 2:
                return "베스트셀러 데이터가 부족합니다."
            
            # 인기 디자인/색상/소재 패턴 파악
            design_pattern = ""
            color_pattern = ""
            material_pattern = ""
            
            # 디자인 패턴 분석
            if 'top_designs' in self.summary and self.summary['top_designs']:
                top_designs = self.summary['top_designs'][:2]
                design_pattern = f"{', '.join(top_designs)}"
            
            # 색상 패턴 분석
            if 'top_colors' in self.summary and self.summary['top_colors']:
                top_colors = [item['name'] for item in self.summary['top_colors'][:2]]
                color_pattern = f"{', '.join(top_colors)}"
            
            # 소재 패턴 분석
            if 'top_materials' in self.summary and self.summary['top_materials']:
                top_materials = self.summary['top_materials'][:2]
                material_pattern = f"{', '.join(top_materials)}"
            
            # 핵심 특성 결합 (소재 추가)
            pattern_elements = []
            if design_pattern:
                pattern_elements.append(f"{design_pattern} 디자인")
            if color_pattern:
                pattern_elements.append(f"{color_pattern} 색상")
            if material_pattern:
                pattern_elements.append(f"{material_pattern} 소재")
            
            pattern_text = ""
            if pattern_elements:
                if len(pattern_elements) > 1:
                    pattern_text = f"{', '.join(pattern_elements[:-1])}과 {pattern_elements[-1]}가 인기입니다."
                else:
                    pattern_text = f"{pattern_elements[0]}가 인기입니다."
            
            # 스타일 트렌드 활용 (패턴이 없는 경우 대체용)
            if not pattern_text and 'auto_style_keywords' in self.summary and self.summary['auto_style_keywords']:
                styles = [item['name'] if isinstance(item, dict) else item 
                        for item in self.summary['auto_style_keywords'][:2]]
                if styles:
                    pattern_text = f"{', '.join(styles)} 스타일이 트렌드입니다."
            
            # 최종 인사이트 구성 (간결하게)
            if pattern_text:
                return pattern_text
            else:
                return "베스트셀러 상품들의 특성을 반영한 신규 상품 개발을 고려해보세요."