# output/data_processor/chart_processor.py
"""
차트 데이터 처리 모듈
"""
from utils import safe_process_data

class ChartProcessor:
    """차트 데이터 처리 (상품, 색상, 가격대, 채널, 사이즈 등)"""
    
    def __init__(self, insights, formatter):
        self.insights = insights
        self.formatter = formatter
    
    def generate_chart_data(self):
        """
        차트용 데이터 전체를 생성하여 딕셔너리로 반환
        (상품/색상/가격대/채널/사이즈/소재/디자인/베스트셀러 등)
        """
        chart_data = {}
        chart_data['product_data'] = self._get_product_data()
        chart_data['color_data'] = self._get_color_data()
        chart_data['price_data'] = self._get_price_data()
        chart_data['channel_data'] = self._get_channel_data()
        chart_data['size_data'] = self._get_size_data()
        # 소재와 디자인을 각각 별도로 추가
        chart_data['material_data'] = self._get_material_data()
        chart_data['design_data'] = self._get_design_data()
        chart_data['bestseller_data'] = self._get_bestseller_data()
        return chart_data

    def _get_product_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'keywords',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="product_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]

    def _get_color_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'colors',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="color_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 1}]

    def _get_price_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'prices',
            default_value=[{'name': '데이터 로드 오류', 'value': 0, 'percent': 0}],
            error_message="price_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0, 'percent': 0}]

    def _get_channel_data(self):
        """채널 데이터 최대 10개까지 추출"""
        channels_data = safe_process_data(
            self.formatter.format_table_data, 'channels',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="channel_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]
        
        # 채널 데이터가 10개보다 적을 경우 모두 반환, 아니면 상위 10개 반환
        return channels_data[:10] if len(channels_data) > 10 else channels_data

    def _get_size_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'sizes',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="size_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 1}]

    def _get_material_data(self):
        """소재 데이터만 추출"""
        return safe_process_data(
            self.formatter.format_table_data, 'materials',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="material_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]

    def _get_design_data(self):
        """디자인 데이터만 추출"""
        return safe_process_data(
            self.formatter.format_table_data, 'designs',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="design_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]

    def _get_material_design_data(self):
        """Legacy method for backward compatibility"""
        try:
            material_data = self._get_material_data()
            design_data = self._get_design_data()
            material_design_data = material_data[:3] + design_data[:3]
            print(f"material_design_data 추출: {len(material_design_data)} 항목")
            return material_design_data or [{'name': '데이터 없음', 'value': 0}]
        except Exception as e:
            print(f"material_design_data 추출 중 오류: {e}")
            return [{'name': '데이터 로드 오류', 'value': 0}]

    def _get_bestseller_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'bestsellers',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="bestseller_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]