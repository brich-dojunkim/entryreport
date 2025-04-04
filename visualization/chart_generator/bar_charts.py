# visualization/chart_generator/bar_charts.py
"""
막대 차트 생성을 위한 클래스
"""
import plotly.express as px
from visualization.chart_generator.base import BaseChartGenerator

class HorizontalBarChart(BaseChartGenerator):
    """
    수평 막대 차트 생성기
    """
    
    def create_chart(self, data, title, **kwargs):
        """
        수평 막대 차트 생성
        
        Parameters:
        - data: 차트 데이터 (딕셔너리 리스트)
        - title: 차트 제목
        - kwargs: 추가 파라미터
        
        Returns:
        - 수평 막대 차트 객체
        """
        if not self.check_data(data):
            return self.create_empty_chart(f"'{title}'에 대한 데이터가 없습니다")
        
        # 기본 x, y축 레이블 설정
        x_label = kwargs.pop('x_label', '값')
        y_label = kwargs.pop('y_label', '항목')
        
        # 데이터 추출
        x_values = [d.get('value', 0) for d in data]
        y_values = [d.get('name', '') for d in data]
        
        # 색상 설정
        color = kwargs.pop('color', self.colors[0])
        
        # 차트 생성
        fig = px.bar(
            data_frame=None,
            x=x_values,
            y=y_values,
            orientation='h',
            labels={'x': x_label, 'y': y_label},
            color_discrete_sequence=[color]
        )
        
        # y축 순서 조정 (값 기준 오름차순)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        # 레이아웃 커스터마이징
        return self.customize_layout(fig, title, **kwargs)


class VerticalBarChart(BaseChartGenerator):
    """
    수직 막대 차트 생성기
    """
    
    def create_chart(self, data, title, **kwargs):
        """
        수직 막대 차트 생성
        
        Parameters:
        - data: 차트 데이터 (딕셔너리 리스트)
        - title: 차트 제목
        - kwargs: 추가 파라미터
        
        Returns:
        - 수직 막대 차트 객체
        """
        if not self.check_data(data):
            return self.create_empty_chart(f"'{title}'에 대한 데이터가 없습니다")
        
        # 기본 x, y축 레이블 설정
        x_label = kwargs.pop('x_label', '항목')
        y_label = kwargs.pop('y_label', '값')
        
        # 데이터 추출
        x_values = [d.get('name', '') for d in data]
        y_values = [d.get('value', 0) for d in data]
        
        # 텍스트 표시 옵션
        text = kwargs.pop('text', None)
        if text is None and 'percent' in data[0]:
            text = [f"{d.get('percent', 0)}%" for d in data]
        
        # 색상 설정
        color = kwargs.pop('color', self.colors[1])
        
        # 차트 생성
        fig = px.bar(
            data_frame=None,
            x=x_values,
            y=y_values,
            labels={'x': x_label, 'y': y_label},
            color_discrete_sequence=[color],
            text=text
        )
        
        # 텍스트 위치 설정
        if text:
            fig.update_traces(
                textposition='outside',
                texttemplate='%{text}'
            )
        
        # 레이아웃 커스터마이징
        return self.customize_layout(fig, title, **kwargs)