import pandas as pd
import numpy as np
import re
from datetime import datetime
from pathlib import Path
from modules.config import STOP_WORDS, CATEGORY_MAPPING, PRODUCT_ATTRIBUTES
from modules.keyword_extractor import KeywordExtractor

class BflowAnalyzer:
    """단순화된 비플로우 주문 데이터 분석 클래스"""
    
    def __init__(self):
        # 결과물 저장 폴더 생성
        self.output_folder = Path('bflow_reports')
        self.output_folder.mkdir(exist_ok=True)
        
        # 차트 저장 폴더 생성
        self.chart_folder = self.output_folder / 'charts'
        self.chart_folder.mkdir(exist_ok=True)
        
        # 현재 시간 (파일명용)
        self.now = datetime.now()
        self.timestamp = self.now.strftime("%Y%m%d_%H%M")
        
        # 분석 결과 저장용 딕셔너리
        self.insights = {}
    
    def load_data(self, file_path1, file_path2=None):
        """데이터 로드 및 전처리"""
        print("데이터 로드 및 전처리 중...")
        # 첫 번째 파일 로드
        df1 = pd.read_excel(file_path1)
        
        # 두 번째 파일이 있으면 로드 후 결합
        if file_path2:
            df2 = pd.read_excel(file_path2)
            self.df = pd.concat([df1, df2], ignore_index=True)
        else:
            self.df = df1
        
        # 기본 전처리
        # 날짜 형식 변환
        self.df['결제일'] = pd.to_datetime(self.df['결제일'], errors='coerce')
        
        # 상품가격을 숫자로 변환
        self.df['상품가격'] = pd.to_numeric(self.df['상품가격'], errors='coerce')
        
        # 상품별 총 주문금액을 숫자로 변환
        self.df['상품별 총 주문금액'] = pd.to_numeric(self.df['상품별 총 주문금액'], errors='coerce')
        
        # 분석 기간 파악
        self.start_date = self.df['결제일'].min().strftime('%Y년 %m월 %d일')
        self.end_date = self.df['결제일'].max().strftime('%Y년 %m월 %d일')
        
        print(f"데이터 로드 완료: 총 {len(self.df)}개의 주문 데이터 ({self.start_date} ~ {self.end_date})")
        
        return self.df
    
    def analyze_data(self):
        """데이터 분석 수행"""
        print("데이터 분석 수행 중...")
        
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
        return self.insights
    
    def analyze_channels(self):
        """판매 채널 분석"""
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
        # 카테고리별 주문 수 계산
        category_counts = self.df['상품 카테고리'].value_counts()
        
        # 상위 10개 카테고리 선택
        top_categories = category_counts.head(10)
        
        # 결과 저장
        self.insights['categories'] = {
            'counts': category_counts,
            'top_categories': top_categories,
            'mapping': CATEGORY_MAPPING,
            'category_data': [{'name': CATEGORY_MAPPING.get(cat, str(cat)[:10]), 'id': cat, 'value': count} 
                            for cat, count in top_categories.items()]
        }
    
    def analyze_product_attributes(self):
        """상품 속성 분석 (키워드, 색상, 사이즈, 소재, 디자인을 통합)"""
        # 1. 상품명 키워드 분석
        self._analyze_product_keywords()
        
        # 2. 색상, 사이즈, 소재, 디자인 분석 (통합 처리)
        for attr_type, keywords in PRODUCT_ATTRIBUTES.items():
            self._analyze_attribute(attr_type, keywords)
    
    def _analyze_product_keywords(self):
        """상품명 키워드 분석"""
        # 키워드 추출
        keywords_dict = {}
        
        for name in self.df['상품명'].dropna():
            # 문자열이 아니면 스킵
            if not isinstance(name, str):
                continue
                
            # 소문자 변환
            name = name.lower()
            
            # 브랜드명 제거 (/ 기준으로 분리)
            parts = name.split('/')
            if len(parts) > 1:
                product_part = parts[1]
            else:
                product_part = name
            
            # 불용어 제거
            for word in STOP_WORDS:
                product_part = product_part.replace(word.lower(), ' ')
            
            # 단어 분리 및 필터링
            words = re.findall(r'\b[가-힣a-zA-Z]{2,}\b', product_part)
            
            # 단어 빈도 카운트
            for word in words:
                if word in keywords_dict:
                    keywords_dict[word] += 1
                else:
                    keywords_dict[word] = 1
        
        # 상위 20개 키워드 선택
        sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)
        top_keywords = sorted_keywords[:20]
        
        # 결과 저장
        self.insights['product_keywords'] = {
            'all_keywords': keywords_dict,
            'top_keywords': top_keywords,
            'keyword_data': [{'name': keyword, 'value': count} 
                           for keyword, count in top_keywords[:10]]
        }
    
    def _analyze_attribute(self, attr_type, keywords):
        """상품 속성(색상, 사이즈, 소재, 디자인) 분석 통합 함수"""
        # 속성 키워드 카운트
        attr_counts = {}
        
        for keyword in keywords:
            # 상품명에서 검색
            name_count = self.df['상품명'].str.contains(keyword, case=False, na=False).sum()
            
            # 옵션정보에서 검색
            option_count = self.df['옵션정보'].str.contains(keyword, case=False, na=False).sum()
            
            # 더 큰 값을 사용 (중복 제거)
            attr_counts[keyword] = max(name_count, option_count)
        
        # 상위 항목 선택
        sorted_items = sorted(attr_counts.items(), key=lambda x: x[1], reverse=True)
        top_items = sorted_items[:10]
        
        # 사이즈의 경우 FREE 비율 계산
        free_size_ratio = 0
        if attr_type == 'sizes':
            total_counts = sum(attr_counts.values())
            if total_counts > 0:
                free_size_ratio = (attr_counts.get('FREE', 0) / total_counts * 100).round(1)
        
        # 결과 저장
        self.insights[attr_type] = {
            'all_items': attr_counts,
            'top_items': top_items,
            f'{attr_type}_data': [{'name': item, 'value': count} 
                                for item, count in top_items[:7]]
        }
        
        # 사이즈의 경우 FREE 비율 추가
        if attr_type == 'sizes':
            self.insights[attr_type]['free_size_ratio'] = free_size_ratio
    
    def analyze_price_ranges(self):
        """가격대별 분석"""
        # 가격대 범주화
        self.df['가격대'] = pd.cut(
            self.df['상품가격'], 
            bins=[0, 10000, 30000, 50000, 100000, float('inf')], 
            labels=['1만원 미만', '1~3만원', '3~5만원', '5~10만원', '10만원 이상']
        )
        
        # 가격대별 주문 수 계산
        price_range_counts = self.df['가격대'].value_counts().sort_index()
        
        # 가격대별 비율 계산
        price_range_percent = (price_range_counts / price_range_counts.sum() * 100).round(1)
        
        # 결과 저장
        self.insights['price_ranges'] = {
            'counts': price_range_counts,
            'percent': price_range_percent,
            'price_data': [{'name': range_name, 'value': count, 'percent': percent} 
                          for range_name, count, percent in zip(
                              price_range_counts.index, 
                              price_range_counts.values, 
                              price_range_percent.values)]
        }
    
    def analyze_bestsellers(self):
        """베스트셀러 상품 분석"""
        # 상품별 주문 건수 계산
        product_counts = self.df['상품명'].value_counts()
        
        # 상위 10개 상품 선택
        top_products = product_counts.head(10)
        
        # 결과 저장
        self.insights['bestsellers'] = {
            'top_products': top_products,
            'bestseller_data': [{'name': product, 'value': count} 
                               for product, count in top_products.head(5).items()]
        }
    
    def analyze_channel_prices(self):
        """채널별 평균 가격 분석"""
        # 채널별 평균 가격 계산
        channel_prices = {}
        for channel in self.insights['channels']['top_channels'].index:
            # 해당 채널 데이터만 필터링
            channel_df = self.df[self.df['판매채널'] == channel]
            
            # 평균 가격 계산 (NaN 값 제외)
            avg_price = channel_df['상품가격'].mean()
            
            # 결과 저장
            channel_prices[channel] = int(round(avg_price))
        
        # 결과 저장
        self.insights['channel_prices'] = channel_prices

    def extract_auto_keywords(self):
        """자동 키워드 추출 및 분석"""
        try:
            # KeywordExtractor 인스턴스 생성
            extractor = KeywordExtractor(self.df)
            
            # 1. 스타일 키워드 자동 추출
            style_keywords = extractor.extract_style_keywords()
            
            # 2. 상품 추가 키워드 추출 (TF-IDF 기반)
            additional_product_keywords = extractor.extract_product_keywords(n_keywords=15)
            
            # 3. 색상 그룹 추출
            color_groups = extractor.extract_color_groups()
            
            # 결과 저장
            self.insights['auto_keywords'] = {
                'style_keywords': style_keywords,
                'additional_product_keywords': additional_product_keywords,
                'color_groups': color_groups
            }
            
            print(f"자동 키워드 추출 완료: {len(style_keywords)} 스타일, {len(additional_product_keywords)} 상품 키워드")
        except Exception as e:
            print(f"자동 키워드 추출 중 오류: {e}")
            self.insights['auto_keywords'] = {}
    
    def get_analysis_summary(self):
        """분석 결과 요약 반환"""
        # 분석 기간
        period = f"{self.start_date} ~ {self.end_date}"
        
        # 총 주문 건수
        total_orders = len(self.df)
        
        # 상위 3개 판매 채널
        top3_channels = ', '.join(self.insights['channels']['top3_channels'])
        top3_ratio = self.insights['channels']['top3_ratio']
        
        # 상위 3개 상품 키워드
        top3_keywords = [keyword for keyword, _ in self.insights['product_keywords']['top_keywords'][:3]]
        top3_keywords_str = ', '.join(top3_keywords)
        
        # 주력 가격대
        main_price_range = self.insights['price_ranges']['counts'].idxmax()
        main_price_percent = self.insights['price_ranges']['percent'][main_price_range]
        
        # 인기 색상 TOP3
        top3_colors = [color for color, _ in self.insights['colors']['top_items'][:3]]
        top3_colors_str = ', '.join(top3_colors)
        
        # 결과 요약
        summary = {
            'period': period,
            'total_orders': total_orders,
            'top3_channels': top3_channels,
            'top3_ratio': top3_ratio,
            'top3_keywords': top3_keywords_str,
            'main_price_range': main_price_range,
            'main_price_percent': main_price_percent,
            'top3_colors': top3_colors_str
        }
        
        return summary