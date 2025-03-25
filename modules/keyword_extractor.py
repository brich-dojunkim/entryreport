from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import re

class KeywordExtractor:
    """상품 데이터에서 자동으로 키워드를 추출하는 클래스"""
    
    def __init__(self, df):
        self.df = df
        
    def extract_product_keywords(self, column='상품명', n_keywords=10):
        """TF-IDF를 이용한 중요 키워드 추출"""
        # 결측치 제거 및 텍스트 전처리
        texts = self.df[column].dropna().astype(str)
        texts = texts.apply(self._preprocess_text)
        
        # TF-IDF 벡터화
        tfidf = TfidfVectorizer(
            max_features=100, 
            min_df=5,
            ngram_range=(1, 2)  # 단어와 구(2단어)까지 추출
        )
        tfidf_matrix = tfidf.fit_transform(texts)
        
        # 각 단어의 평균 TF-IDF 점수 계산
        feature_names = tfidf.get_feature_names_out()
        tfidf_scores = tfidf_matrix.mean(axis=0).A1
        
        # 상위 키워드 추출
        top_indices = tfidf_scores.argsort()[-n_keywords:][::-1]
        top_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
        
        return top_keywords
    
    def extract_style_keywords(self, column='상품명', n_clusters=5, n_keywords=3):
        """클러스터링을 통한 스타일 키워드 자동 추출"""
        # 결측치 제거 및 텍스트 전처리
        texts = self.df[column].dropna().astype(str)
        texts = texts.apply(self._preprocess_text)
        
        # 용어 빈도수 벡터화
        count_vec = CountVectorizer(max_features=200, min_df=3)
        term_matrix = count_vec.fit_transform(texts)
        
        # K-means 클러스터링
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(term_matrix)
        
        # 각 클러스터별 주요 키워드 추출
        feature_names = count_vec.get_feature_names_out()
        style_keywords = []
        
        for i in range(n_clusters):
            # 해당 클러스터 문서 인덱스
            cluster_doc_indices = np.where(clusters == i)[0]
            
            if len(cluster_doc_indices) > 0:
                # 클러스터 내 문서들의 단어 빈도 합계
                cluster_term_freq = term_matrix[cluster_doc_indices].sum(axis=0).A1
                # 상위 키워드 추출
                top_indices = cluster_term_freq.argsort()[-n_keywords:][::-1]
                cluster_keywords = [feature_names[idx] for idx in top_indices]
                style_keywords.append(cluster_keywords)
        
        # 모든 클러스터의 키워드를 1차원 리스트로 변환
        flattened_keywords = [kw for cluster in style_keywords for kw in cluster]
        
        return flattened_keywords
    
    def extract_color_groups(self, n_clusters=4):
        """색상 데이터 클러스터링을 통한 색상 그룹 추출"""
        if '옵션정보' not in self.df.columns:
            return []
            
        # 색상 데이터 추출 (옵션정보에서 색상 정보 추출)
        option_texts = self.df['옵션정보'].dropna().astype(str)
        
        # 색상 키워드 추출을 위한 패턴
        from modules.config import PRODUCT_ATTRIBUTES
        color_patterns = '|'.join(PRODUCT_ATTRIBUTES['colors'])
        color_regex = re.compile(r'(' + color_patterns + r')', re.IGNORECASE)
        
        # 색상 추출 및 빈도 계산
        colors = []
        for text in option_texts:
            matches = color_regex.findall(text)
            colors.extend(matches)
        
        color_counts = pd.Series(colors).value_counts()
        
        # 상위 색상 선택
        top_colors = color_counts.head(20)
        
        return [(color, count) for color, count in top_colors.items()]
    
    def _preprocess_text(self, text):
        """텍스트 전처리"""
        # 소문자 변환
        text = text.lower()
        
        # 불용어 제거 (기존 STOP_WORDS 사용)
        from modules.config import STOP_WORDS
        for word in STOP_WORDS:
            text = text.replace(word.lower(), ' ')
        
        # 추가 전처리 (특수문자 제거 등)
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        
        return text