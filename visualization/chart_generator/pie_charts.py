# visualization/chart_generator/pie_charts.py
"""
파이 차트 생성을 위한 클래스
"""
import plotly.express as px
from visualization.chart_generator.base import BaseChartGenerator

class PieChart(BaseChartGenerator):
    """
    파이 차트 생성기
    """
    
    def create_chart(self, data, title, **kwargs):
        """
        파이 차트 생성
        
        Parameters:
        - data: 차트 데이터 (딕셔너리 리스트)
        - title: 차트 제목
        - kwargs: 추가 파라미터
        
        Returns:
        - 파이 차트 객체
        """
        if not self.check_data(data):
            return self.create_empty_chart(f"'{title}'에 대한 데이터가 없습니다")
        
        # 홀 크기 설정 (0: 파이 차트, >0: 도넛 차트)
        hole = kwargs.pop('hole', 0.4)
        
        # 데이터 추출
        values = [d.get('value', 0) for d in data]
        names = [d.get('name', '') for d in data]
        
        # 차트 생성
        fig = px.pie(
            data_frame=None,
            values=values,
            names=names,
            color_discrete_sequence=self.colors
        )
        
        # 도넛 차트 설정
        fig.update_traces(
            hole=hole,
            textposition='inside',
            textinfo='percent+label'
        )
        
        # 레이아웃 커스터마이징
        return self.customize_layout(fig, title, **kwargs)