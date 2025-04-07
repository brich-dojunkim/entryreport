"""
키워드 추출 메인 클래스 - KeywordExtractor
"""
import re

# 절대 경로 import (사용자 요청사항)
from config import Config
from utils import clean_text, safe_process_data
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
        self.config = config if config is not None else Config()
    
    def extract_product_keywords(self, column='상품명', n_keywords=10, use_category=True):
        """
        TF-IDF를 이용한 중요 키워드 추출  
        카테고리 정보가 있으면 카테고리별 추출, 없으면 전체 데이터 추출
        
        Parameters:
        - column: 텍스트 컬럼명
        - n_keywords: 추출할 키워드 수
        - use_category: 카테고리 정보 활용 여부
        
        Returns:
        - [(키워드, tfidf값), ...] 형태의 리스트
        """
        if column not in self.df.columns:
            return []
        
        # 카테고리별 TF-IDF 키워드 추출 (카테고리 컬럼이 있고 use_category가 True인 경우)
        if use_category and '상품 카테고리' in self.df.columns:
            return safe_process_data(
                TfidfExtractor.extract_category_tfidf_keywords,
                self.df, '상품 카테고리', column, n_keywords,
                default_value=[],
                error_message=f"카테고리별 {column} 키워드 추출 중 오류"
            )
        
        # 전체 데이터 TF-IDF 키워드 추출
        texts = self._prepare_texts(column)
        if texts is None or len(texts) == 0:
            return []
        
        return safe_process_data(
            TfidfExtractor.extract_tfidf_keywords,
            texts, n_keywords,
            default_value=[],
            error_message=f"{column} 키워드 추출 중 오류"
        )
    
    def extract_style_keywords(self, column='상품명', n_clusters=5, n_keywords=3):
        """클러스터링을 통한 스타일 키워드 자동 추출"""
        texts = self._prepare_texts(column)
        if texts is None or len(texts) == 0:
            return []
        
        return safe_process_data(
            ClusterExtractor.extract_cluster_keywords,
            texts, n_clusters, n_keywords,
            default_value=[],
            error_message=f"{column} 스타일 키워드 추출 중 오류"
        )
    
    def extract_color_groups(self):
        """색상 데이터 클러스터링을 통한 색상 그룹 추출"""
        # '옵션정보' 컬럼이 없으면 불가능
        if '옵션정보' not in self.df.columns:
            return []
        
        option_texts = self.df['옵션정보'].dropna().astype(str)
        if option_texts.empty:
            return []
        
        # 색상 키워드 목록 -> 정규식 패턴으로 결합
        color_patterns = '|'.join(self.config.get_product_attributes('colors'))
        
        return safe_process_data(
            ColorExtractor.extract_color_groups,
            option_texts, color_patterns,
            default_value=[],
            error_message="색상 그룹 추출 중 오류"
        )
    
    def _prepare_texts(self, column):
        """텍스트 데이터 전처리: utils의 clean_text() 사용"""
        if column not in self.df.columns:
            return None
        
        texts = self.df[column].dropna().astype(str)
        if texts.empty:
            return None
        
        # 각 텍스트에 대해 utils의 clean_text 함수를 사용하여 전처리 수행
        cleaned_texts = [clean_text(text) for text in texts]
        return cleaned_texts
