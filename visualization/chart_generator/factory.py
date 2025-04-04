# visualization/chart_generator/factory.py
"""
차트 생성 팩토리 클래스
"""
from visualization.chart_generator.bar_charts import HorizontalBarChart, VerticalBarChart
from visualization.chart_generator.pie_charts import PieChart

class ChartFactory:
    """
    차트 생성 팩토리
    차트 유형에 따라 적절한 생성기를 반환합니다.
    """
    
    @staticmethod
    def get_chart_generator(chart_type, colors=None):
        """
        차트 유형에 따른 차트 생성기 반환
        
        Parameters:
        - chart_type: 차트 유형 (horizontal_bar, vertical_bar, pie)
        - colors: 차트 색상 (지정하지 않으면 기본 색상 사용)
        
        Returns:
        - 차트 생성기 객체
        """
        if chart_type == 'horizontal_bar':
            return HorizontalBarChart(colors)
        elif chart_type == 'vertical_bar':
            return VerticalBarChart(colors)
        elif chart_type == 'pie':
            return PieChart(colors)
        else:
            raise ValueError(f"지원하지 않는 차트 유형: {chart_type}")
