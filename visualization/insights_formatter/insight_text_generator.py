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
        return "데이터 분석 중..."
