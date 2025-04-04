# modules/analyzer.py
import pandas as pd
from datetime import datetime
from config.config import Config
from data.data_processor.data_processor import DataProcessor
from data.keyword_extractor import KeywordExtractor

class BflowAnalyzer:
    """비플로우 주문 데이터 분석 클래스"""
    
    def __init__(self, config=None):
        """
        Parameters:
        - config: 설정 객체
        """
        # 설정 객체 설정
        self.config = config if config is not None else Config()
        
        # 데이터 프로세서 생성
        self.data_processor = DataProcessor(self.config)
        
        # 결과물 저장 폴더 생성
        self.output_folder = self.config.create_output_folders()
        self.chart_folder = self.output_folder / 'charts'
        
        # 현재 시간 (파일명용)
        self.now = datetime.now()
        self.timestamp = self.now.strftime("%Y%m%d_%H%M")
        
        # 분석 결과 저장용 딕셔너리
        self.insights = {}
        
        # 데이터프레임 참조
        self.df = None
    
    def load_data(self, file_path1, file_path2=None):
        """
        데이터 로드 및 전처리 (DataProcessor에 위임)
        
        Parameters:
        - file_path1: 첫 번째 엑셀 파일 경로
        - file_path2: 두 번째 엑셀 파일 경로 (선택사항)
        
        Returns:
        - 전처리된 데이터프레임
        """
        self.df = self.data_processor.load_data(file_path1, file_path2)
        self.start_date, self.end_date = self.data_processor.get_analysis_period()
        return self.df
    
    def analyze_data(self):
        """
        데이터 분석 수행
        
        Returns:
        - 분석 결과가 담긴 딕셔너리
        """
        if self.df is None or len(self.df) == 0:
            print("분석할 데이터가 없습니다. load_data 메소드를 먼저 호출하세요.")
            return {}
        
        print("데이터 분석 수행 중...")
        
        try:
            # 1. 판매 채널 분석
            self.analyze_channels()
            
            # 2. 카테고리 분석
            self.analyze_categories()
            
            # 3. 상품 속성 분석 (키워드, 색상, 사이즈, 소재, 디자인 통합)
            self.analyze_product_attributes()
            
            # 4. 가격대 분석
            self.analyze_price_ranges()
            
            # 5. 베스트셀러 상품 분석
            self.analyze_bestsellers()
            
            # 6. 채널별 평균 가격 분석
            self.analyze_channel_prices()
            
            # 7. 자동 키워드 추출 추가
            self.extract_auto_keywords()
            
            # 분석 시작/종료 날짜 정보 저장
            self.insights['start_date'] = self.start_date
            self.insights['end_date'] = self.end_date
            
            # 데이터프레임 저장 (다른 모듈에서 참조할 수 있도록)
            self.insights['df'] = self.df
            
            print("데이터 분석 완료")
            
        except Exception as e:
            print(f"데이터 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        return self.insights
    
    def analyze_channels(self):
        """판매 채널 분석"""
        # 데이터 프로세서에 위임
        channel_counts, top_channels, top3_ratio, top3_channel_list, channel_data = self.data_processor.get_channel_data()
        
        # 결과 저장
        self.insights['channels'] = {
            'counts': channel_counts,
            'top_channels': top_channels,
            'top3_ratio': top3_ratio,
            'top3_channels': top3_channel_list,
            'channel_data': channel_data
        }
    
    def analyze_categories(self):
        """카테고리 분석"""
        if '상품 카테고리' not in self.df.columns:
            self.insights['categories'] = {'counts': pd.Series(), 'top_categories': pd.Series()}
            return
            
        # 카테고리별 주문 수 계산
        category_counts = self.df['상품 카테고리'].value_counts()
        
        # 상위 10개 카테고리 선택
        top_categories = category_counts.head(10)
        
        # 결과 저장
        self.insights['categories'] = {
            'counts': category_counts,
            'top_categories': top_categories,
            'mapping': self.config.CATEGORY_MAPPING,
            'category_data': [{'name': self.config.get_category_name(cat), 'id': cat, 'value': count} 
                            for cat, count in top_categories.items()]
        }
    
    def analyze_product_attributes(self):
        """상품 속성 분석 (키워드, 색상, 사이즈, 소재, 디자인 통합)"""
        # 상품 키워드 분석
        self.analyze_product_keywords()
        
        # 색상 분석
        self.analyze_colors()
        
        # 사이즈 분석
        self.analyze_sizes()
        
        # 소재 분석
        self.analyze_materials()
        
        # 디자인 요소 분석
        self.analyze_designs()
    
    def analyze_product_keywords(self):
        """상품 키워드 분석"""
        # 데이터 프로세서에 위임
        top_keywords = self.data_processor.extract_product_keywords()
        
        # 결과 저장
        self.insights['product_keywords'] = {
            'top_keywords': top_keywords
        }
    
    def analyze_colors(self):
        """색상 분석"""
        # 데이터 프로세서에 위임
        top_colors = self.data_processor.extract_colors()
        
        # 데이터 포맷팅
        colors_data = []
        for color, count in top_colors:
            colors_data.append({
                'name': color,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        # 결과 저장
        self.insights['colors'] = {
            'top_items': top_colors,
            'colors_data': colors_data
        }
    
    def analyze_sizes(self):
        """사이즈 분석"""
        # 데이터 프로세서에 위임
        top_sizes, free_size_ratio = self.data_processor.extract_sizes()
        
        # 데이터 포맷팅
        sizes_data = []
        for size, count in top_sizes:
            sizes_data.append({
                'name': size,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        # 결과 저장
        self.insights['sizes'] = {
            'top_items': top_sizes,
            'free_size_ratio': free_size_ratio,
            'sizes_data': sizes_data
        }
    
    def analyze_materials(self):
        """소재 분석"""
        # 데이터 프로세서에 위임
        top_materials = self.data_processor.extract_materials()
        
        # 데이터 포맷팅
        materials_data = []
        for material, count in top_materials:
            materials_data.append({
                'name': material,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        # 결과 저장
        self.insights['materials'] = {
            'top_items': top_materials,
            'materials_data': materials_data
        }
    
    def analyze_designs(self):
        """디자인 요소 분석"""
        # 데이터 프로세서에 위임
        top_designs = self.data_processor.extract_designs()
        
        # 데이터 포맷팅
        designs_data = []
        for design, count in top_designs:
            designs_data.append({
                'name': design,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        # 결과 저장
        self.insights['designs'] = {
            'top_items': top_designs,
            'designs_data': designs_data
        }
    
    def analyze_price_ranges(self):
        """가격대 분석"""
        # 데이터 프로세서에 위임
        price_counts, price_percent, price_data = self.data_processor.analyze_price_ranges()
        
        # 결과 저장
        self.insights['price_ranges'] = {
            'counts': price_counts,
            'percent': price_percent,
            'price_data': price_data
        }
    
    def analyze_bestsellers(self):
        """베스트셀러 상품 분석"""
        # 데이터 프로세서에 위임
        top_products, bestseller_data = self.data_processor.analyze_bestsellers()
        
        # 결과 저장
        self.insights['bestsellers'] = {
            'top_products': top_products,
            'bestseller_data': bestseller_data
        }
    
    def analyze_channel_prices(self):
        """채널별 평균 가격 분석"""
        # 데이터 프로세서에 위임
        channel_prices = self.data_processor.analyze_channel_prices()
        
        # 결과 저장
        self.insights['channel_prices'] = channel_prices
    
    def extract_auto_keywords(self):
        """자동 키워드 추출"""
        if self.df is None or len(self.df) == 0:
            self.insights['auto_keywords'] = {}
            return
            
        try:
            # KeywordExtractor 인스턴스 생성
            extractor = KeywordExtractor(self.df, self.config)
            
            # 스타일 키워드 추출
            style_keywords = extractor.extract_style_keywords('상품명', n_clusters=5, n_keywords=3)
            
            # 추가 상품 키워드 추출
            additional_keywords = extractor.extract_product_keywords('상품명', n_keywords=15)
            
            # 색상 그룹 추출
            color_groups = extractor.extract_color_groups(n_clusters=4)
            
            # 결과 저장
            self.insights['auto_keywords'] = {
                'style_keywords': style_keywords,
                'additional_product_keywords': additional_keywords,
                'color_groups': color_groups
            }
        except Exception as e:
            print(f"자동 키워드 추출 중 오류 발생: {e}")
            self.insights['auto_keywords'] = {}