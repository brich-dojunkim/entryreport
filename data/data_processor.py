# modules/data_processor.py
import pandas as pd
import numpy as np
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

class DataProcessor:
    """데이터 로딩 및 전처리를 담당하는 클래스"""
    
    def __init__(self, config=None):
        """
        Parameters:
        - config: 설정 객체
        """
        from config.config import Config
        self.config = config if config is not None else Config()
        self.df = None
        self.start_date = None
        self.end_date = None
    
    def load_data(self, file_path1, file_path2=None):
        """
        데이터 로드 및 기본 전처리
        
        Parameters:
        - file_path1: 첫 번째 엑셀 파일 경로
        - file_path2: 두 번째 엑셀 파일 경로 (선택사항)
        
        Returns:
        - 전처리된 데이터프레임
        """
        print("데이터 로드 및 전처리 중...")
        
        try:
            # 첫 번째 파일 로드
            df1 = pd.read_excel(file_path1)
            
            # 두 번째 파일이 있으면 로드 후 결합
            if file_path2:
                df2 = pd.read_excel(file_path2)
                self.df = pd.concat([df1, df2], ignore_index=True)
            else:
                self.df = df1
            
            # 기본 전처리 수행
            self._preprocess_data()
            
            print(f"데이터 로드 완료: 총 {len(self.df)}개의 주문 데이터 ({self.start_date} ~ {self.end_date})")
            
            return self.df
            
        except Exception as e:
            print(f"데이터 로드 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()  # 빈 데이터프레임 반환
    
    def _preprocess_data(self):
        """기본 데이터 전처리 수행"""
        # 날짜 형식 변환
        if '결제일' in self.df.columns:
            self.df['결제일'] = pd.to_datetime(self.df['결제일'], errors='coerce')
            
            # 분석 기간 파악
            if not self.df['결제일'].isna().all():
                self.start_date = self.df['결제일'].min().strftime('%Y년 %m월 %d일')
                self.end_date = self.df['결제일'].max().strftime('%Y년 %m월 %d일')
            else:
                self.start_date = "알 수 없음"
                self.end_date = "알 수 없음"
        
        # 상품가격을 숫자로 변환
        if '상품가격' in self.df.columns:
            self.df['상품가격'] = pd.to_numeric(self.df['상품가격'], errors='coerce')
        
        # 상품별 총 주문금액을 숫자로 변환
        if '상품별 총 주문금액' in self.df.columns:
            self.df['상품별 총 주문금액'] = pd.to_numeric(self.df['상품별 총 주문금액'], errors='coerce')
        
        # 결측치 처리
        self._handle_missing_data()
        
        # 중복 데이터 제거
        self._remove_duplicates()
    
    def _handle_missing_data(self):
        """결측치 처리"""
        # 필수 컬럼에 결측치가 있는 행 제거
        essential_columns = ['결제일', '상품명']
        self.df = self.df.dropna(subset=essential_columns)
        
        # 상품가격 결측치는 0으로 대체
        if '상품가격' in self.df.columns:
            self.df['상품가격'] = self.df['상품가격'].fillna(0)
    
    def _remove_duplicates(self):
        """중복 데이터 제거"""
        # 주문 ID와 상품 ID 기준 중복 제거 (있는 경우)
        if '주문번호' in self.df.columns and '상품번호' in self.df.columns:
            self.df = self.df.drop_duplicates(subset=['주문번호', '상품번호'])
        elif '주문번호' in self.df.columns:
            self.df = self.df.drop_duplicates(subset=['주문번호'])
    
    def get_analysis_period(self):
        """분석 기간 반환"""
        return self.start_date, self.end_date
    
    def extract_product_keywords(self):
        """상품명에서 키워드 추출"""
        if '상품명' not in self.df.columns:
            return []
        
        # 불용어 목록 가져오기
        stop_words = self.config.get_stop_words()
        
        # 전처리 함수
        def preprocess_product_name(name):
            if not isinstance(name, str):
                return ""
            # 소문자 변환 및 특수문자 제거
            name = name.lower()
            # 불용어 제거
            for word in stop_words:
                name = name.replace(word.lower(), ' ')
            # 특수문자 제거 (알파벳, 숫자, 한글, 공백만 남김)
            name = re.sub(r'[^\w\s가-힣]', ' ', name)
            # 연속된 공백 제거
            name = re.sub(r'\s+', ' ', name).strip()
            return name
        
        # 상품명 전처리
        processed_names = self.df['상품명'].astype(str).apply(preprocess_product_name)
        
        # 단어 추출 및 빈도 계산
        all_words = []
        for name in processed_names:
            words = re.findall(r'\b[가-힣a-zA-Z]{2,}\b', name)  # 2글자 이상 단어만 추출
            all_words.extend(words)
        
        # 빈도수 계산
        word_counts = Counter(all_words)
        
        # 상위 키워드 추출
        top_keywords = word_counts.most_common(20)
        
        return top_keywords
    
    def extract_colors(self):
        """옵션정보에서 색상 추출"""
        if '옵션정보' not in self.df.columns:
            return []
        
        # 색상 키워드 목록 가져오기
        color_keywords = self.config.get_product_attributes('colors')
        
        # 옵션정보에서 색상 추출
        colors = []
        for option in self.df['옵션정보'].dropna().astype(str):
            for color in color_keywords:
                if color in option:
                    colors.append(color)
                    break
        
        # 색상별 빈도 계산
        color_counts = Counter(colors)
        
        # 상위 색상 추출
        top_colors = color_counts.most_common(10)
        
        return top_colors
    
    def extract_sizes(self):
        """옵션정보에서 사이즈 추출"""
        if '옵션정보' not in self.df.columns:
            return []
        
        # 사이즈 키워드 목록 가져오기
        size_keywords = self.config.get_product_attributes('sizes')
        
        # 옵션정보에서 사이즈 추출
        sizes = []
        for option in self.df['옵션정보'].dropna().astype(str):
            for size in size_keywords:
                if size in option:
                    sizes.append(size)
                    break
        
        # 사이즈별 빈도 계산
        size_counts = Counter(sizes)
        
        # 상위 사이즈 추출
        top_sizes = size_counts.most_common(10)
        
        # FREE 사이즈 비율 계산
        free_size_count = size_counts.get('FREE', 0)
        free_size_ratio = (free_size_count / sum(size_counts.values()) * 100) if size_counts else 0
        
        return top_sizes, free_size_ratio
    
    def extract_materials(self):
        """상품명과 상세설명에서 소재 추출"""
        # 소재 키워드 목록 가져오기
        material_keywords = self.config.get_product_attributes('materials')
        
        materials = []
        
        # 상품명에서 추출
        if '상품명' in self.df.columns:
            for name in self.df['상품명'].dropna().astype(str):
                for material in material_keywords:
                    if material in name:
                        materials.append(material)
                        break
        
        # 상품상세설명에서 추출 (있는 경우)
        if '상품상세설명' in self.df.columns:
            for desc in self.df['상품상세설명'].dropna().astype(str):
                for material in material_keywords:
                    if material in desc:
                        materials.append(material)
                        break
        
        # 소재별 빈도 계산
        material_counts = Counter(materials)
        
        # 상위 소재 추출
        top_materials = material_counts.most_common(10)
        
        return top_materials
    
    def extract_designs(self):
        """상품명과 상세설명에서 디자인 요소 추출"""
        # 디자인 키워드 목록 가져오기
        design_keywords = self.config.get_product_attributes('designs')
        
        designs = []
        
        # 상품명에서 추출
        if '상품명' in self.df.columns:
            for name in self.df['상품명'].dropna().astype(str):
                for design in design_keywords:
                    if design in name:
                        designs.append(design)
                        break
        
        # 상품상세설명에서 추출 (있는 경우)
        if '상품상세설명' in self.df.columns:
            for desc in self.df['상품상세설명'].dropna().astype(str):
                for design in design_keywords:
                    if design in desc:
                        designs.append(design)
                        break
        
        # 디자인별 빈도 계산
        design_counts = Counter(designs)
        
        # 상위 디자인 추출
        top_designs = design_counts.most_common(10)
        
        return top_designs
    
    def analyze_price_ranges(self):
        """가격대 분석"""
        if '상품가격' not in self.df.columns:
            return pd.Series(), pd.Series(), []
        
        # 가격대 구간 정의
        price_bins = [0, 10000, 20000, 30000, 50000, 70000, 100000, 150000, 200000, 1000000]
        price_labels = [
            '1만원 미만', '1~2만원', '2~3만원', '3~5만원', 
            '5~7만원', '7~10만원', '10~15만원', '15~20만원', '20만원 이상'
        ]
        
        # 가격대별 상품 수 계산
        price_counts = pd.cut(
            self.df['상품가격'], 
            bins=price_bins, 
            labels=price_labels, 
            right=False
        ).value_counts().sort_index()
        
        # 가격대별 비율 계산
        price_percent = (price_counts / price_counts.sum() * 100).round(1)
        
        # 데이터 포맷팅
        price_data = []
        for price_range, count in price_counts.items():
            percent = price_percent[price_range]
            price_data.append({
                'name': price_range,
                'value': count,
                'percent': percent,
                'range': price_range
            })
        
        return price_counts, price_percent, price_data
    
    def analyze_bestsellers(self):
        """베스트셀러 상품 분석"""
        if '상품명' not in self.df.columns:
            return pd.Series(), []
        
        # 상품별 주문 수 계산
        product_counts = self.df['상품명'].value_counts()
        
        # 상위 10개 상품 선택
        top_products = product_counts.head(10)
        
        # 데이터 포맷팅
        bestseller_data = []
        for idx, (product, count) in enumerate(top_products.items(), 1):
            # 상품명이 너무 길면 잘라서 표시
            display_name = product
            if len(product) > 50:
                display_name = product[:47] + "..."
                
            bestseller_data.append({
                'rank': idx,
                'name': display_name,
                'product': product,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        return top_products, bestseller_data
    
    def analyze_channel_prices(self):
        """채널별 평균 가격 분석"""
        if '판매채널' not in self.df.columns or '상품가격' not in self.df.columns:
            return {}
            
        # 채널별 평균 가격 계산
        channel_prices = self.df.groupby('판매채널')['상품가격'].mean()
        
        return channel_prices.to_dict()
    
    def get_channel_data(self):
        """판매 채널 분석"""
        if '판매채널' not in self.df.columns:
            return pd.Series(), pd.Series(), 0, [], []
            
        # 채널별 주문 수 계산
        channel_counts = self.df['판매채널'].value_counts()
        
        # 상위 5개 채널 선택
        top_channels = channel_counts.head(5)
        
        # 전체 주문 중 상위 3개 채널의 비율 계산
        top3_channels = channel_counts.head(3)
        top3_ratio = (top3_channels.sum() / channel_counts.sum() * 100).round(1)
        
        # 채널 리스트
        top3_channel_list = top3_channels.index.tolist()
        
        # 데이터 포맷팅
        channel_data = []
        for channel, count in top_channels.items():
            channel_data.append({
                'name': channel,
                'value': count
            })
            
        return channel_counts, top_channels, top3_ratio, top3_channel_list, channel_data