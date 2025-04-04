# dashboard_generator/data_processor/insight_processor.py
"""
인사이트 텍스트 생성 처리 모듈
"""

class InsightProcessor:
    """인사이트 텍스트 처리 클래스"""
    
    def __init__(self, formatter):
        """
        인사이트 처리기 초기화
        
        Parameters:
        - formatter: InsightsFormatter 인스턴스
        """
        self.formatter = formatter
    
    def generate_insights(self):
        """
        모든 섹션의 인사이트 텍스트 생성
        
        Returns:
        - 인사이트 텍스트 딕셔너리
        """
        insights = {}
        
        # 각 섹션별 인사이트 텍스트 생성
        insights['product_insight'] = self.formatter.generate_insight_text('product')
        insights['color_insight'] = self.formatter.generate_insight_text('color')
        insights['price_insight'] = self.formatter.generate_insight_text('price')
        insights['channel_insight'] = self.formatter.generate_insight_text('channel')
        insights['size_insight'] = self.formatter.generate_insight_text('size')
        insights['material_design_insight'] = self.formatter.generate_insight_text('material_design')
        
        return insights