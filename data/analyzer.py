# data/analyzer.py
import pandas as pd
from datetime import datetime
from config.config import Config
from data.data_processor.data_processor import DataProcessor
from data.keyword_extractor import KeywordExtractor

class BflowAnalyzer:
    """비플로우 주문 데이터 분석 클래스 (DataProcessor의 기능을 활용하여 결과 통합)"""
    
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
        """
        데이터 로드 및 전처리 (DataProcessor에 위임)
        
        Parameters:
          - file_path: 엑셀 파일 경로
        
        Returns:
          - 전처리된 데이터프레임
        """
        self.df = self.data_processor.load_data(file_path)
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
            
            # 2. 카테고리 분석 (직접 처리)
            self._analyze_categories()
            
            # 3. 상품 속성 분석
            self.insights['product_keywords'] = {
                'top_keywords': self.data_processor.extract_product_keywords()
            }
            self.insights['colors'] = self._format_items(self.data_processor.extract_colors())
            
            sizes, free_size_ratio = self.data_processor.extract_sizes()
            self.insights['sizes'] = {
                'top_items': sizes,
                'free_size_ratio': free_size_ratio,
                'formatted': self._format_items(sizes)
            }
            self.insights['materials'] = self._format_items(self.data_processor.extract_materials())
            self.insights['designs'] = self._format_items(self.data_processor.extract_designs())
            
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
            
            # 5. 자동 키워드 추출
            self._extract_auto_keywords()
            
            # 6. 전체 데이터프레임 저장 (후속 모듈 참조용)
            self.insights['df'] = self.df
            
            print("데이터 분석 완료")
        except Exception as e:
            print(f"데이터 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        return self.insights
        
    def _analyze_categories(self):
        """카테고리 분석 (추가 처리)"""
        if '상품 카테고리' not in self.df.columns:
            # 빈 Series를 넣는 것은 문제 없음
            self.insights['categories'] = {
                'counts': pd.Series(dtype=int),
                'top_categories': pd.Series(dtype=int)
            }
            return
        
        category_counts = self.df['상품 카테고리'].value_counts()
        top_categories = category_counts.head(10)
        self.insights['categories'] = {
            'counts': category_counts,
            'top_categories': top_categories,
            'mapping': self.config.CATEGORY_MAPPING,
            'category_data': [
                {
                    'name': self.config.get_category_name(cat),
                    'id': cat,
                    'value': count
                } 
                for cat, count in top_categories.items()
            ]
        }
    
    def _format_items(self, items):
        """
        리스트 형식의 (이름, 개수) 튜플을
        차트용 포맷(딕셔너리 리스트)으로 변환
        """
        formatted = []
        for name, count in items:
            formatted.append({'name': name, 'count': count, 'value': count})
        return formatted
    
    def _extract_auto_keywords(self):
        """
        자동 키워드 추출 (KeywordExtractor 활용)
        """
        if self.df is None or self.df.empty:
            self.insights['auto_keywords'] = {}
            return
        
        try:
            extractor = KeywordExtractor(self.df, self.config)
            
            # 스타일 키워드
            style_keywords = extractor.extract_style_keywords(
                column='상품명',
                n_clusters=5,
                n_keywords=3
            )
            # 상품 키워드
            additional_keywords = extractor.extract_product_keywords(
                column='상품명',
                n_keywords=15
            )
            # 색상 그룹 (원본 코드에서 n_clusters=4였지만, 
            # keyword_extractor.py에선 파라미터가 없으므로 제거/수정)
            color_groups = extractor.extract_color_groups()
            
            self.insights['auto_keywords'] = {
                'style_keywords': style_keywords,
                'additional_product_keywords': additional_keywords,
                'color_groups': color_groups
            }
            
            # 디버깅용 출력
            print("[디버그] 자동 키워드 추출 결과:")
            print("style_keywords:", style_keywords)
            print("additional_product_keywords:", additional_keywords)
            print("color_groups:", color_groups)
            
        except Exception as e:
            print(f"자동 키워드 추출 중 오류 발생: {e}")
            self.insights['auto_keywords'] = {}
