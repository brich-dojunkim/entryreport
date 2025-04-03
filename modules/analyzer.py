# modules/analyzer.py
import pandas as pd
import numpy as np
import re
from datetime import datetime
from pathlib import Path
from modules.config import Config
from modules.data_processor import DataProcessor
from modules.keyword_extractor import KeywordExtractor

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
    
    # 나머지 분석 메소드들은 현재 코드를 유지하거나 약간의 개선을 할 수 있습니다.
    # 예를 들어, Config 객체를 사용하도록 변경할 수 있습니다.
    
    def analyze_channels(self):
        """판매 채널 분석"""
        if '판매채널' not in self.df.columns:
            self.insights['channels'] = {'counts': pd.Series(), 'top_channels': pd.Series()}
            return
            
        # 채널별 주문 수 계산
        channel_counts = self.df['판매채널'].value_counts()
        
        # 상위 5개 채널 선택
        top_channels = channel_counts.head(5)
        
        # 전체 주문 중 상위 3개 채널의 비율 계산
        top3_channels = channel_counts.head(3)
        top3_ratio = (top3_channels.sum() / channel_counts.sum() * 100).round(1)
        
        # 결과 저장
        self.insights['channels'] = {
            'counts': channel_counts,
            'top_channels': top_channels,
            'top3_ratio': top3_ratio,
            'top3_channels': top3_channels.index.tolist(),
            'channel_data': [{'name': channel, 'value': count} 
                            for channel, count in top_channels.items()]
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
    
    # 나머지 분석 메소드들도 필요한 경우 Config 객체 사용 등의 변경을 할 수 있습니다.