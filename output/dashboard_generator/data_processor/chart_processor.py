# dashboard_generator/data_processor/chart_processor.py
"""
차트 데이터 처리 모듈
"""
from utils.utils import safe_process_data

class ChartProcessor:
    """차트 데이터 처리 클래스"""
    
    def __init__(self, insights, formatter):
        """
        차트 처리기 초기화
        
        Parameters:
        - insights: 분석 결과 딕셔너리
        - formatter: InsightsFormatter 인스턴스
        """
        self.insights = insights
        self.formatter = formatter
    
    def generate_chart_data(self):
        """
        모든 차트 데이터 생성
        
        Returns:
        - 차트 데이터 딕셔너리
        """
        chart_data = {}
        
        # 상품 차트 데이터
        chart_data['product_data'] = self._get_product_data()
        
        # 색상 차트 데이터
        chart_data['color_data'] = self._get_color_data()
        
        # 가격대 차트 데이터
        chart_data['price_data'] = self._get_price_data()
        
        # 판매 채널 차트 데이터
        chart_data['channel_data'] = self._get_channel_data()
        
        # 사이즈 차트 데이터
        chart_data['size_data'] = self._get_size_data()
        
        # 소재 및 디자인 차트 데이터
        chart_data['material_design_data'] = self._get_material_design_data()
        
        # 베스트셀러 차트 데이터
        chart_data['bestseller_data'] = self._get_bestseller_data()
        
        return chart_data
    
    def _get_product_data(self):
        """상품 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'keywords',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="product_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 0}]
    
    def _get_color_data(self):
        """색상 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'colors',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="color_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 1}]
    
    def _get_price_data(self):
        """가격대 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'prices',
            default_value=[{'name': '데이터 로드 오류', 'value': 0, 'percent': 0}],
            error_message="price_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 0, 'percent': 0}]
    
    def _get_channel_data(self):
        """채널 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'channels',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="channel_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 0}]
    
    def _get_size_data(self):
        """사이즈 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'sizes',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="size_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 1}]
    
    def _get_material_design_data(self):
        """소재 및 디자인 차트 데이터 생성"""
        try:
            material_data = self.formatter.format_table_data('materials')
            design_data = self.formatter.format_table_data('designs')
            material_data = material_data if material_data else []
            design_data = design_data if design_data else []
            material_design_data = material_data[:3] + design_data[:3]
            print(f"material_design_data 추출: {len(material_design_data)} 항목")
            return material_design_data if material_design_data else [{'name': '데이터 없음', 'value': 0}]
        except Exception as e:
            print(f"material_design_data 추출 중 오류: {e}")
            return [{'name': '데이터 로드 오류', 'value': 0}]
    
    def _get_bestseller_data(self):
        """베스트셀러 차트 데이터 생성"""
        data = safe_process_data(
            self.formatter.format_table_data, 'bestsellers',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="bestseller_data 추출 중 오류"
        )
        return data if data else [{'name': '데이터 없음', 'value': 0}]