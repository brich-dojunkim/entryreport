# config/__init__.py
"""
비플로우 분석 시스템의 설정 관리 모듈
"""
from .keyword_config import KeywordConfig
from .product_config import ProductConfig
from .category_config import CategoryConfig
from .output_config import OutputConfig

class Config:
    """
    모든 설정을 통합하는 클래스
    """
    
    def __init__(self):
        """
        모든 설정 모듈 초기화
        """
        self.keyword_config = KeywordConfig()
        self.product_config = ProductConfig()
        self.category_config = CategoryConfig()
        self.output_config = OutputConfig()
        
        # 출력 관련 설정을 메인 클래스에 복사
        self.output_folder = self.output_config.output_folder
        self.dashboard_port = self.output_config.dashboard_port
        self.report_port = self.output_config.report_port
        self.template_folder = self.output_config.template_folder
    
    # 키워드 관련 메서드
    def get_stop_words(self):
        """불용어 목록 반환"""
        return self.keyword_config.get_stop_words()
    
    def get_non_fashion_keywords(self):
        """비패션 키워드 목록 반환"""
        return self.keyword_config.get_non_fashion_keywords()
    
    def get_fashion_patterns(self):
        """패션 관련 패턴 목록 반환"""
        return self.keyword_config.get_fashion_patterns()
    
    def get_fashion_keywords(self):
        """패션 관련 키워드 목록 반환"""
        return self.keyword_config.get_fashion_keywords()
    
    # 제품 속성 관련 메서드
    def get_product_attributes(self, attr_type=None):
        """제품 속성 반환"""
        return self.product_config.get_attribute(attr_type)
    
    # 카테고리 관련 메서드
    def get_category_name(self, category_code):
        """카테고리 코드에 대한 이름 반환"""
        return self.category_config.get_category_name(category_code)
    
    # 차트 색상 메서드는 기존 호환성을 위해 유지하되, 하드코딩된 기본값 사용
    def get_chart_colors(self):
        """차트 색상 목록 반환"""
        return ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']
    
    # 출력 관련 메서드
    def create_output_folders(self):
        """필요한 출력 폴더 생성"""
        return self.output_config.create_output_folders()