# output/data_processor/insight_processor.py
"""
인사이트 텍스트 생성 처리 모듈
"""
class InsightProcessor:
    """인사이트 텍스트 처리 (상품, 색상, 가격대, 채널, 사이즈 등)"""
    
    def __init__(self, formatter):
        self.formatter = formatter
    
    def generate_insights(self):
        """
        섹션별 인사이트 텍스트를 생성해 딕셔너리로 반환
        예: product_insight, color_insight, price_insight...
        """
        insights = {}
        insights['product_insight'] = self.formatter.generate_insight_text('product')
        insights['color_insight'] = self.formatter.generate_insight_text('color')
        insights['price_insight'] = self.formatter.generate_insight_text('price')
        insights['channel_insight'] = self.formatter.generate_insight_text('channel')
        insights['size_insight'] = self.formatter.generate_insight_text('size')
        insights['material_design_insight'] = self.formatter.generate_insight_text('material_design')
        
        return insights
