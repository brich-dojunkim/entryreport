# modules/data_processor.py
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

class DataProcessor:
    """데이터 로딩 및 전처리를 담당하는 클래스"""
    
    def __init__(self, config=None):
        """
        Parameters:
        - config: 설정 객체
        """
        from modules.config import Config
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
            self.df['상품가격'].fillna(0, inplace=True)
    
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