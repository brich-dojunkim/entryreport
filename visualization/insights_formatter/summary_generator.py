# visualization/insights_formatter/summary_generator.py
"""
요약 정보를 바탕으로 인사이트 문장을 생성하는 모듈
"""
class SummaryGenerator:
    """
    요약 정보를 바탕으로 사람이 읽을 수 있는 인사이트 문장을 생성하는 클래스
    """
    def __init__(self, summary):
        self.summary = summary

    def generate_summary_insights(self):
        """
        요약 정보를 바탕으로 사람이 읽을 수 있는 인사이트 문장들을 생성합니다.
        
        Returns:
            list: 인사이트 문장 리스트
        """
        summary_points = []
        
        # 상품 키워드 정보 추가
        if self.summary.get('top_keywords'):
            kw0 = self.summary['top_keywords'][0]
            summary_points.append(f"가장 많이 팔린 상품군: {kw0['name']} ({kw0['count']}건 판매)")
            
            # 인기 키워드 더 포함
            if len(self.summary['top_keywords']) > 1:
                kw_names = [item['name'] for item in self.summary['top_keywords'][:3]]
                summary_points.append(f"인기 키워드: {', '.join(kw_names)}")
        
        # 채널 정보 추가
        if self.summary.get('top3_channels'):
            summary_points.append(f"주요 판매 채널: {', '.join(self.summary['top3_channels'])}")
            
            # 채널 점유율 포함
            if 'top3_ratio' in self.summary:
                summary_points.append(f"상위 3개 채널 점유율: {self.summary['top3_ratio']}%")
        
        # 가격대 정보 추가
        if self.summary.get('main_price_range'):
            summary_points.append(f"주력 가격대: {self.summary['main_price_range']} (전체의 {self.summary.get('main_price_percent', 0):.1f}%)")
        
        # 색상 정보
        if self.summary.get('top_colors'):
            color_names = [item['name'] for item in self.summary['top_colors'][:3]]
            summary_points.append(f"인기 색상: {', '.join(color_names)}")
        
        # 사이즈 정보
        if self.summary.get('free_size_ratio'):
            summary_points.append(f"FREE 사이즈 비율: {self.summary['free_size_ratio']:.1f}%")
        
        return summary_points