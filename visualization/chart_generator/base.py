# visualization/chart_generator/base.py
"""
차트 생성 모듈의 기본 클래스 및 유틸리티 함수
"""
import plotly.graph_objects as go
from config.config import Config

class BaseChartGenerator:
    """
    모든 차트 생성기의 기본 클래스
    공통 기능을 제공하고 추상 메소드를 정의합니다.
    """
    
    # 공통 색상 설정
    DEFAULT_COLORS = Config().get_chart_colors()
    
    def __init__(self, colors=None):
        """
        기본 차트 생성기 초기화
        
        Parameters:
        - colors: 차트 색상 (지정하지 않으면 기본 색상 사용)
        """
        self.colors = colors if colors is not None else self.DEFAULT_COLORS
    
    def create_chart(self, data, title, **kwargs):
        """
        차트 생성 메소드 (하위 클래스에서 구현)
        
        Parameters:
        - data: 차트 데이터
        - title: 차트 제목
        - kwargs: 추가 파라미터
        
        Returns:
        - Plotly 차트 객체
        """
        raise NotImplementedError("하위 클래스에서 구현해야 합니다.")
    
    def customize_layout(self, fig, title, height=400, **kwargs):
        """
        차트 레이아웃 커스터마이징
        
        Parameters:
        - fig: Plotly 차트 객체
        - title: 차트 제목
        - height: 차트 높이
        - kwargs: 추가 레이아웃 속성
        
        Returns:
        - 커스터마이징된 차트 객체
        """
        layout = {
            'title': title,
            'margin': dict(l=20, r=20, t=40, b=20),
            'height': height
        }
        
        # 추가 레이아웃 속성 적용
        layout.update(kwargs)
        
        fig.update_layout(**layout)
        return fig
    
    def create_empty_chart(self, message="데이터가 없습니다", height=400):
        """
        빈 차트 생성
        
        Parameters:
        - message: 표시할 메시지
        - height: 차트 높이
        
        Returns:
        - 빈 차트 객체
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(height=height)
        return fig
    
    def check_data(self, data):
        """
        데이터 유효성 검사
        
        Parameters:
        - data: 검사할 데이터
        
        Returns:
        - 데이터 유효성 여부
        """
        return data is not None and len(data) > 0

    def save_chart_to_file(self, fig, file_path, format='png', width=800, height=600):
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