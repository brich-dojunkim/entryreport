# data/keyword_extractor/keyword_extractor.py
"""
키워드 추출 메인 클래스 - KeywordExtractor
"""
import pandas as pd
import numpy as np

# 절대 경로 import (사용자 요청사항)
from config.config import Config
from utils.utils import clean_text, safe_process_data

# 서브 모듈에서 필요한 static 메서드를 import
from data.keyword_extractor.tfidf_extractor import TfidfExtractor
from data.keyword_extractor.cluster_extractor import ClusterExtractor
from data.keyword_extractor.color_extractor import ColorExtractor

class KeywordExtractor:
    """상품 데이터에서 자동으로 키워드를 추출하는 클래스"""
    
    def __init__(self, df, config=None):
        """
        Parameters:
        - df: 분석할 데이터프레임
        - config: 설정 객체
        """
        self.df = df
        if config is None:
            self.config = Config()
        else:
            self.config = config
    
    def extract_product_keywords(self, column='상품명', n_keywords=10):
        """TF-IDF를 이용한 중요 키워드 추출"""
        texts = self._prepare_texts(column)
        if not texts or len(texts) == 0:
            return []
        
        # 서브 모듈의 static 메서드를 safe_process_data로 감싸 호출
        return safe_process_data(
            TfidfExtractor.extract_tfidf_keywords,
            texts, n_keywords,
            default_value=[],
            error_message=f"{column} 키워드 추출 중 오류"
        )
    
    def extract_style_keywords(self, column='상품명', n_clusters=5, n_keywords=3):
        """클러스터링을 통한 스타일 키워드 자동 추출"""
        texts = self._prepare_texts(column)
        if not texts or len(texts) == 0:
            return []
        
        return safe_process_data(
            ClusterExtractor.extract_cluster_keywords,
            texts, n_clusters, n_keywords,
            default_value=[],
            error_message=f"{column} 스타일 키워드 추출 중 오류"
        )
    
    def extract_color_groups(self, n_clusters=4):
        """색상 데이터 클러스터링을 통한 색상 그룹 추출"""
        if '옵션정보' not in self.df.columns:
            return []
        
        option_texts = self.df['옵션정보'].dropna().astype(str)
        if option_texts.empty:
            return []
        
        # 색상 키워드 목록 -> 정규식
        color_patterns = '|'.join(self.config.get_product_attributes('colors'))
        
        return safe_process_data(
            ColorExtractor.extract_color_groups,
            option_texts, color_patterns,
            default_value=[],
            error_message="색상 그룹 추출 중 오류"
        )
    
    def _prepare_texts(self, column):
        """텍스트 데이터 준비 및 전처리"""
        if column not in self.df.columns:
            return None
        
        texts = self.df[column].dropna().astype(str)
        if texts.empty:
            return None
        
        # 전처리 함수 적용
        return texts.apply(self._preprocess_text)
    
    def _preprocess_text(self, text):
        """텍스트 전처리"""
        # utils.clean_text 사용
        return clean_text(text, self.config.get_stop_words())
