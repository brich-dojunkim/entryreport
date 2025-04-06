# output/data_processor/chart_processor.py
"""
차트 데이터 처리 모듈
"""
from utils.utils import safe_process_data  # 사용처에 맞춰 절대경로 or 상대경로 조정

class ChartProcessor:
    """차트 데이터 처리 (상품, 색상, 가격대, 채널, 사이즈 등)"""
    
    def __init__(self, insights, formatter):
        self.insights = insights
        self.formatter = formatter
    
    def generate_chart_data(self):
        """
        차트용 데이터 전체를 생성하여 딕셔너리로 반환
        (상품/색상/가격대/채널/사이즈/소재/베스트셀러 등)
        """
        chart_data = {}
        chart_data['product_data'] = self._get_product_data()
        chart_data['color_data'] = self._get_color_data()
        chart_data['price_data'] = self._get_price_data()
        chart_data['channel_data'] = self._get_channel_data()
        chart_data['size_data'] = self._get_size_data()
        chart_data['material_design_data'] = self._get_material_design_data()
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
        return safe_process_data(
            self.formatter.format_table_data, 'channels',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="channel_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 0}]

    def _get_size_data(self):
        return safe_process_data(
            self.formatter.format_table_data, 'sizes',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="size_data 추출 중 오류"
        ) or [{'name': '데이터 없음', 'value': 1}]

    def _get_material_design_data(self):
        try:
            material_data = self.formatter.format_table_data('materials') or []
            design_data = self.formatter.format_table_data('designs') or []
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
