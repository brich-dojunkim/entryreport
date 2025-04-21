# data/data_processor/data_processor.py
import pandas as pd
from config import Config
from data.data_processor.data_loader import DataLoader
from data.data_processor.attribute_extractor import AttributeExtractor
from data.data_processor.sales_analyzer import SalesAnalyzer

class DataProcessor:
    """데이터 로딩 및 전처리를 담당하는 클래스 - 통합 인터페이스 제공"""
    
    def __init__(self, config=None):
        """
        Parameters:
        - config: 설정 객체
        """
        self.config = config if config is not None else Config()
        
        # 하위 프로세서 생성
        self.data_loader = DataLoader(self.config)
        self.df = None
        self.start_date = None
        self.end_date = None
        
        # AttributeExtractor와 SalesAnalyzer는 데이터가 로드된 후 초기화됨
        self.attribute_extractor = None
        self.sales_analyzer = None
    
    def load_data(self, file_path):
        """
        데이터 로드 및 기본 전처리
        
        Parameters:
        - file_path: 엑셀 파일 경로
        
        Returns:
        - 전처리된 데이터프레임
        """
        # DataLoader에 위임
        self.df = self.data_loader.load_data(file_path)
        self.start_date, self.end_date = self.data_loader.get_analysis_period()
        
        # 데이터 로드 후 나머지 프로세서 초기화
        if self.df is not None and not self.df.empty:
            self.attribute_extractor = AttributeExtractor(self.df, self.config)
            self.sales_analyzer = SalesAnalyzer(self.df, self.config)
        
        return self.df
    
    def filter_allowed_categories(self):
        """CSV에 정의된 카테고리의 상품만 필터링"""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        if '상품 카테고리' not in self.df.columns:
            return self.df
        
        # 디버깅을 위한 출력 추가
        print(f"필터링 전 카테고리 샘플: {self.df['상품 카테고리'].head(10).tolist()}")
        print(f"필터링 전 카테고리 타입: {self.df['상품 카테고리'].dtype}")
        
        # CSV에 정의된 카테고리에 속하는 상품만 필터링
        def is_allowed(code):
            if pd.isna(code):
                return False
            if isinstance(code, (int, float)):
                code = str(int(code))
            else:
                code = str(code)
            result = self.config.category_config.is_allowed_category(code)
            # 디버깅을 위한 출력
            if result:
                print(f"허용된 카테고리: {code}")
            return result
        
        filtered_df = self.df[self.df['상품 카테고리'].apply(is_allowed)]
        
        print(f"전체 {len(self.df)}개 상품 중 {len(filtered_df)}개의 허용된 카테고리 상품 발견")
        
        if len(filtered_df) == 0:
            # 디버깅: 허용된 카테고리 목록 출력
            print(f"허용된 카테고리 목록: {list(self.config.category_config.allowed_categories)[:10]}...")
        
        self.df = filtered_df
        if self.df is not None and not self.df.empty:
            self.attribute_extractor = AttributeExtractor(self.df, self.config)
            self.sales_analyzer = SalesAnalyzer(self.df, self.config)
        
        return self.df    
    
    def get_analysis_period(self):
        """분석 기간 반환"""
        return self.start_date, self.end_date
    
    # AttributeExtractor 메소드에 위임
    def extract_product_keywords(self):
        """상품명에서 키워드 추출"""
        if self.attribute_extractor is None:
            return []
        return self.attribute_extractor.extract_product_keywords()
    
    def extract_colors(self):
        """옵션정보에서 색상 추출"""
        if self.attribute_extractor is None:
            return []
        return self.attribute_extractor.extract_colors()
    
    def extract_sizes(self):
        """옵션정보에서 사이즈 추출"""
        if self.attribute_extractor is None:
            return [], 0
        return self.attribute_extractor.extract_sizes()
    
    def extract_materials(self):
        """상품명과 상세설명에서 소재 추출"""
        if self.attribute_extractor is None:
            return []
        return self.attribute_extractor.extract_materials()
    
    def extract_designs(self):
        """상품명과 상세설명에서 디자인 요소 추출"""
        if self.attribute_extractor is None:
            return []
        return self.attribute_extractor.extract_designs()
    
    # SalesAnalyzer 메소드에 위임
    def get_channel_data(self):
        """판매 채널 분석"""
        if self.sales_analyzer is None:
            return pd.Series(), pd.Series(), 0, [], []
        return self.sales_analyzer.get_channel_data()
    
    def analyze_price_ranges(self):
        """가격대 분석"""
        if self.sales_analyzer is None:
            return pd.Series(), pd.Series(), []
        return self.sales_analyzer.analyze_price_ranges()
    
    def analyze_bestsellers(self):
        """베스트셀러 상품 분석"""
        if self.sales_analyzer is None:
            return pd.Series(), []
        return self.sales_analyzer.analyze_bestsellers()
    
    def analyze_channel_prices(self):
        """채널별 평균 가격 분석"""
        if self.sales_analyzer is None:
            return {}
        return self.sales_analyzer.analyze_channel_prices()
    
    def analyze_categories(self):
        """카테고리 분석"""
        if self.sales_analyzer is None:
            return pd.Series(), pd.Series(), []
        return self.sales_analyzer.analyze_categories()