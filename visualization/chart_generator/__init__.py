# visualization/chart_generator/__init__.py
"""
차트 생성 모듈
"""
from visualization.chart_generator.factory import ChartFactory
from visualization.chart_generator.base import BaseChartGenerator

# 주요 함수 - 이름을 ChartGenerator로 하여 기존 코드와 호환성 유지
def ChartGenerator(chart_type, data, colors=None):
    """
    차트 생성 함수
    
    Parameters:
    - chart_type: 차트 유형 (product, color, price, channel, size, material_design, bestseller)
    - data: 차트 데이터
    - colors: 차트 색상 (지정하지 않으면 기본 색상 사용)
    
    Returns:
    - Plotly 차트 객체
    """
    # 타이틀 설정
    title_mapping = {
        'product': '인기 상품 유형 TOP10',
        'color': '인기 색상 TOP7',
        'price': '가격대별 상품 분포',
        'channel': '주요 판매 채널',
        'size': '사이즈 분포',
        'material_design': '인기 소재 & 디자인 요소',
        'bestseller': '베스트셀러 상품'
    }
    
    title = title_mapping.get(chart_type, f'{chart_type} 차트')
    
    # 차트 유형 매핑 및 생성
    type_mapping = {
        'product': 'horizontal_bar',
        'bestseller': 'horizontal_bar',
        'color': 'pie',
        'size': 'pie',
        'price': 'vertical_bar',
        'channel': 'vertical_bar',
        'material_design': 'vertical_bar'
    }
    
    # 차트 유형이 매핑에 없으면 기본 생성기 반환
    generator_type = type_mapping.get(chart_type)
    if not generator_type:
        base_generator = BaseChartGenerator(colors)
        return base_generator.create_empty_chart(f"지원하지 않는 차트 유형: {chart_type}")
    
    # 팩토리를 통해 차트 생성기 가져오기
    generator = ChartFactory.get_chart_generator(generator_type, colors)
    
    # 차트 유형별 추가 설정
    kwargs = {}
    if chart_type == 'product':
        kwargs.update({
            'x_label': '키워드 빈도',
            'y_label': '상품 유형',
            'color': colors[0] if colors else None
        })
    elif chart_type == 'bestseller':
        kwargs.update({
            'x_label': '주문 수',
            'y_label': '상품명',
            'color': colors[3] if colors else None
        })
    # ... 다른 차트 유형들에 대한 처리 ...
    
    # 차트 생성
    return generator.create_chart(data, title, **kwargs)

# 유틸리티 함수들
def create_empty_chart(message="데이터가 없습니다"):
    """빈 차트 생성"""
    generator = BaseChartGenerator()
    return generator.create_empty_chart(message)

def save_chart_to_file(fig, file_path, format='png', width=800, height=600):
    """차트를 파일로 저장"""
    generator = BaseChartGenerator()
    return generator.save_chart_to_file(fig, file_path, format, width, height)

# 기존 코드와의 호환성을 위해 ChartGenerator 함수에 유틸리티 메소드도 추가
ChartGenerator.create_empty_chart = create_empty_chart
ChartGenerator.save_chart_to_file = save_chart_to_file