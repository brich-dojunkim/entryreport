import pandas as pd
from datetime import datetime
from config import Config
from data.data_processor.data_processor import DataProcessor

# 동료 모듈을 상대 경로로 import
from . import category_analyzer, keyword_analyzer, utils

class BflowAnalyzer:
    """비플로우 주문 데이터 분석 클래스 (모듈화된 각 기능을 활용하여 결과 통합)"""
    
    def __init__(self, config=None):
        """
        Parameters:
          - config: 설정 객체
        """
        self.config = config if config is not None else Config()
        self.data_processor = DataProcessor(self.config)
        self.output_folder = self.config.create_output_folders()
        self.chart_folder = self.output_folder / 'charts'
        self.now = datetime.now()
        self.timestamp = self.now.strftime("%Y%m%d_%H%M")
        self.insights = {}
        self.df = None
    
    def load_data(self, file_path):
        """데이터 로드 및 전처리 (허용된 카테고리만 필터링)"""
        self.df = self.data_processor.load_data(file_path)
        
        # CSV에 정의된 카테고리의 상품만 필터링
        self.df = self.data_processor.filter_allowed_categories()
        
        self.insights['start_date'], self.insights['end_date'] = self.data_processor.get_analysis_period()
        return self.df
    
    def analyze_data(self):
        """
        데이터 분석 수행 및 최종 인사이트 조합
        
        Returns:
          - 분석 결과(insights) 딕셔너리
        """
        if self.df is None or self.df.empty:
            print("분석할 데이터가 없습니다. load_data 메소드를 먼저 호출하세요.")
            return {}
        
        print("데이터 분석 수행 중...")
        
        try:
            # 1. 판매 채널 분석
            channels = self.data_processor.get_channel_data()
            self.insights['channels'] = {
                'counts': channels[0],
                'top_channels': channels[1],
                'top3_ratio': channels[2],
                'top3_channels': channels[3],
                'channel_data': channels[4]
            }
            
            # 2. 카테고리 분석 (모듈화된 함수 호출)
            self.insights['categories'] = category_analyzer.analyze_categories(self.df, self.config)
            
            # 3. 상품 속성 분석
            self.insights['product_keywords'] = {
                'top_keywords': self.data_processor.extract_product_keywords()
            }
            self.insights['colors'] = utils.format_items(self.data_processor.extract_colors())
            
            sizes, free_size_ratio = self.data_processor.extract_sizes()
            self.insights['sizes'] = {
                'top_items': sizes,
                'free_size_ratio': free_size_ratio,
                'formatted': utils.format_items(sizes)
            }
            self.insights['materials'] = utils.format_items(self.data_processor.extract_materials())
            self.insights['designs'] = utils.format_items(self.data_processor.extract_designs())
            
            # 4. 가격대, 베스트셀러, 채널별 가격 분석
            price_ranges = self.data_processor.analyze_price_ranges()
            self.insights['price_ranges'] = {
                'counts': price_ranges[0],
                'percent': price_ranges[1],
                'price_data': price_ranges[2]
            }
            bestsellers = self.data_processor.analyze_bestsellers()
            self.insights['bestsellers'] = {
                'top_products': bestsellers[0],
                'bestseller_data': bestsellers[1]
            }
            self.insights['channel_prices'] = self.data_processor.analyze_channel_prices()
            
            # 5. 자동 키워드 추출 (모듈화된 함수 호출)
            self.insights['auto_keywords'] = keyword_analyzer.extract_auto_keywords(self.df, self.config)
            
            # 6. 전체 데이터프레임 저장 (후속 모듈 참조용)
            self.insights['df'] = self.df
            
            print("데이터 분석 완료")
        except Exception as e:
            print(f"데이터 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        return self.insights
