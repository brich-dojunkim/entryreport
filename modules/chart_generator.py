import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from modules.config import CHART_COLORS

class ChartGenerator:
    """
    분석 결과를 바탕으로 다양한 차트를 생성하는 유틸리티 클래스
    """
    
    # 기본 차트 색상을 config에서 가져온 값으로 설정
    DEFAULT_COLORS = CHART_COLORS
    
    @staticmethod
    def create_chart(chart_type, data, colors=None):
        """
        차트 생성 통합 메소드
        
        Parameters:
        - chart_type: 차트 유형 (product, color, price, channel, size, material_design, bestseller)
        - data: 차트 데이터
        - colors: 차트 색상 (지정하지 않으면 기본 색상 사용)
        
        Returns:
        - Plotly 차트 객체
        """
        # 색상이 지정되지 않은 경우 기본 색상 사용
        if colors is None:
            colors = ChartGenerator.DEFAULT_COLORS
        
        # 데이터가 없는 경우 빈 차트 반환
        if not data or len(data) == 0:
            return ChartGenerator.create_empty_chart("데이터가 없습니다")
            
        # 차트 유형에 따라 적절한 생성 메소드 호출
        if chart_type == 'product':
            return ChartGenerator.create_product_chart(data, colors)
        elif chart_type == 'color':
            return ChartGenerator.create_color_chart(data, colors)
        elif chart_type == 'price':
            return ChartGenerator.create_price_chart(data, colors)
        elif chart_type == 'channel':
            return ChartGenerator.create_channel_chart(data, colors)
        elif chart_type == 'size':
            return ChartGenerator.create_size_chart(data, colors)
        elif chart_type == 'material_design':
            return ChartGenerator.create_material_design_chart(data, colors)
        elif chart_type == 'bestseller':
            return ChartGenerator.create_bestseller_chart(data, colors)
        else:
            return ChartGenerator.create_empty_chart(f"지원하지 않는 차트 유형: {chart_type}")
    
    @staticmethod
    def create_empty_chart(message="데이터가 없습니다"):
        """
        빈 차트 생성
        
        Parameters:
        - message: 표시할 메시지
        
        Returns:
        - 빈 차트 객체
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(height=400)
        return fig
    
    @staticmethod
    def create_product_chart(data, colors):
        """
        상품 유형 차트 생성
        
        Parameters:
        - data: 상품 유형 데이터
        - colors: 차트 색상
        
        Returns:
        - 상품 유형 차트 객체
        """
        fig = px.bar(
            data, 
            x=[d['value'] for d in data], 
            y=[d['name'] for d in data],
            orientation='h',
            labels={'x': '키워드 빈도', 'y': '상품 유형'},
            title='인기 상품 유형 TOP10',
            color_discrete_sequence=[colors[0]]
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_color_chart(data, colors):
        """
        색상 분포 차트 생성
        
        Parameters:
        - data: 색상 데이터
        - colors: 차트 색상
        
        Returns:
        - 색상 분포 차트 객체
        """
        fig = px.pie(
            data,
            values=[d['value'] for d in data],
            names=[d['name'] for d in data],
            title='인기 색상 TOP7',
            color_discrete_sequence=colors
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hole=0.4
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_price_chart(data, colors):
        """
        가격대 분포 차트 생성
        
        Parameters:
        - data: 가격대 데이터
        - colors: 차트 색상
        
        Returns:
        - 가격대 분포 차트 객체
        """
        fig = px.bar(
            data,
            x=[d['name'] for d in data],
            y=[d['value'] for d in data],
            title='가격대별 상품 분포',
            labels={'x': '가격대', 'y': '상품 수'},
            color_discrete_sequence=[colors[1]],
            text=[f"{d['percent']}%" for d in data]
        )
        fig.update_traces(
            textposition='outside',
            texttemplate='%{text}'
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_channel_chart(data, colors):
        """
        판매 채널 차트 생성
        
        Parameters:
        - data: 판매 채널 데이터
        - colors: 차트 색상
        
        Returns:
        - 판매 채널 차트 객체
        """
        fig = px.bar(
            data,
            x=[d['name'] for d in data],
            y=[d['value'] for d in data],
            title='주요 판매 채널',
            labels={'x': '채널', 'y': '주문 수'},
            color_discrete_sequence=[colors[2]]
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_size_chart(data, colors):
        """
        사이즈 분포 차트 생성
        
        Parameters:
        - data: 사이즈 데이터
        - colors: 차트 색상
        
        Returns:
        - 사이즈 분포 차트 객체
        """
        fig = px.pie(
            data,
            values=[d['value'] for d in data],
            names=[d['name'] for d in data],
            title='사이즈 분포',
            color_discrete_sequence=colors
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_material_design_chart(data, colors):
        """
        소재 및 디자인 요소 차트 생성
        
        Parameters:
        - data: 소재 및 디자인 요소 데이터
        - colors: 차트 색상
        
        Returns:
        - 소재 및 디자인 요소 차트 객체
        """
        fig = px.bar(
            data,
            x=[d['name'] for d in data],
            y=[d['value'] for d in data],
            title='인기 소재 & 디자인 요소',
            labels={'x': '소재/디자인', 'y': '빈도'},
            color_discrete_sequence=[colors[4]]
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def create_bestseller_chart(data, colors):
        """
        베스트셀러 상품 차트 생성
        
        Parameters:
        - data: 베스트셀러 상품 데이터
        - colors: 차트 색상
        
        Returns:
        - 베스트셀러 상품 차트 객체
        """
        # 상품명 길이 제한 (너무 길면 차트에서 보기 어려움)
        processed_data = []
        for item in data:
            processed_item = item.copy()
            if len(item['name']) > 30:
                processed_item['name'] = item['name'][:27] + "..."
            processed_data.append(processed_item)
        
        fig = px.bar(
            processed_data,
            x=[d['value'] for d in processed_data],
            y=[d['name'] for d in processed_data],
            orientation='h',
            title='베스트셀러 상품',
            labels={'x': '주문 수', 'y': '상품명'},
            color_discrete_sequence=[colors[3]]
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        return fig
    
    @staticmethod
    def save_chart_to_file(fig, file_path, format='png', width=800, height=600):
        """
        차트를 파일로 저장
        
        Parameters:
        - fig: 차트 객체
        - file_path: 저장할 파일 경로
        - format: 파일 포맷 (png, jpeg, svg, pdf)
        - width: 이미지 너비
        - height: 이미지 높이
        
        Returns:
        - 저장된 파일 경로
        """
        try:
            fig.write_image(file_path, format=format, width=width, height=height)
            return file_path
        except Exception as e:
            print(f"차트 저장 중 오류 발생: {e}")
            return None