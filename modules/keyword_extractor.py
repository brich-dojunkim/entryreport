from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from modules.utils import clean_text, extract_keywords, safe_process_data

class KeywordExtractor:
    """상품 데이터에서 자동으로 키워드를 추출하는 클래스"""
    
    def __init__(self, df, config=None):
        """
        Parameters:
        - df: 분석할 데이터프레임
        - config: 설정 객체
        """
        self.df = df
        
        # 설정 객체 설정
        if config is None:
            from modules.config import Config
            self.config = Config()
        else:
            self.config = config
    
    def extract_product_keywords(self, column='상품명', n_keywords=10):
        """TF-IDF를 이용한 중요 키워드 추출"""
        # 결측치 제거 및 텍스트 전처리
        texts = self._prepare_texts(column)
        if texts is None or len(texts) == 0:
            return []
        
        # TF-IDF 벡터화 및 키워드 추출
        return safe_process_data(
            self._extract_tfidf_keywords, 
            texts, n_keywords,
            default_value=[],
            error_message=f"{column} 키워드 추출 중 오류"
        )
    
    def extract_style_keywords(self, column='상품명', n_clusters=5, n_keywords=3):
        """클러스터링을 통한 스타일 키워드 자동 추출"""
        # 결측치 제거 및 텍스트 전처리
        texts = self._prepare_texts(column)
        if texts is None or len(texts) == 0:
            return []
        
        # 클러스터링 및 키워드 추출
        return safe_process_data(
            self._extract_cluster_keywords, 
            texts, n_clusters, n_keywords,
            default_value=[],
            error_message=f"{column} 스타일 키워드 추출 중 오류"
        )
    
    def extract_color_groups(self, n_clusters=4):
        """색상 데이터 클러스터링을 통한 색상 그룹 추출"""
        if '옵션정보' not in self.df.columns:
            return []
            
        # 색상 데이터 추출 (옵션정보에서 색상 정보 추출)
        option_texts = self.df['옵션정보'].dropna().astype(str)
        
        # 빈 데이터 체크
        if option_texts.empty:
            return []
        
        # 색상 키워드 추출을 위한 패턴
        color_patterns = '|'.join(self.config.get_product_attributes('colors'))
        
        return safe_process_data(
            self._extract_color_groups, 
            option_texts, color_patterns,
            default_value=[],
            error_message="색상 그룹 추출 중 오류"
        )
    
    def _prepare_texts(self, column):
        """텍스트 데이터 준비 및 전처리"""
        if column not in self.df.columns:
            return None
            
        texts = self.df[column].dropna().astype(str)
        
        # 빈 데이터 체크
        if texts.empty:
            return None
            
        return texts.apply(self._preprocess_text)
    
    def _preprocess_text(self, text):
        """텍스트 전처리"""
        # utils.clean_text 사용
        return clean_text(text, self.config.get_stop_words())
    
    def _extract_tfidf_keywords(self, texts, n_keywords=10):
        """TF-IDF로 키워드 추출"""
        # 텍스트 데이터가 없는 경우 빈 리스트 반환
        if len(texts) == 0:
            return []
            
        # TF-IDF 벡터화
        tfidf = TfidfVectorizer(
            max_features=100, 
            min_df=5,
            ngram_range=(1, 2)  # 단어와 구(2단어)까지 추출
        )
        
        try:
            tfidf_matrix = tfidf.fit_transform(texts)
        except ValueError:
            # 데이터가 적절하지 않은 경우 빈 리스트 반환
            return []
        
        # 각 단어의 평균 TF-IDF 점수 계산
        feature_names = tfidf.get_feature_names_out()
        tfidf_scores = tfidf_matrix.mean(axis=0).A1
        
        # 상위 키워드 추출
        top_indices = tfidf_scores.argsort()[-n_keywords:][::-1]
        top_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
        
        return top_keywords
    
    def _extract_cluster_keywords(self, texts, n_clusters=5, n_keywords=3):
        """클러스터링을 통한 키워드 추출"""
        # 텍스트 데이터가 너무 적은 경우 클러스터링 불가
        if len(texts) < n_clusters:
            return []
            
        try:
            # 용어 빈도수 벡터화
            count_vec = CountVectorizer(max_features=200, min_df=3)
            term_matrix = count_vec.fit_transform(texts)
            
            # 특성이 너무 적은 경우 처리
            if term_matrix.shape[1] < 5:
                return []
                
            # K-means 클러스터링
            kmeans = KMeans(n_clusters=min(n_clusters, len(texts) // 5 + 1), random_state=42)
            clusters = kmeans.fit_predict(term_matrix)
            
            # 각 클러스터별 주요 키워드 추출
            feature_names = count_vec.get_feature_names_out()
            style_keywords = []
            
            for i in range(kmeans.n_clusters):
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
        except Exception as e:
            print(f"클러스터링 중 오류 발생: {e}")
            return []
    
    def _extract_color_groups(self, option_texts, color_patterns):
        """옵션 텍스트에서 색상 그룹 추출"""
        import re
        
        # 옵션 텍스트가 없는 경우 빈 리스트 반환
        if len(option_texts) == 0:
            return []
            
        color_regex = re.compile(r'(' + color_patterns + r')', re.IGNORECASE)
        
        # 색상 추출 및 빈도 계산
        colors = []
        for text in option_texts:
            matches = color_regex.findall(text)
            colors.extend(matches)
        
        # 색상이 추출되지 않은 경우 처리
        if not colors:
            return []
            
        color_counts = pd.Series(colors).value_counts()
        
        # 상위 색상 선택
        top_colors = color_counts.head(20)
        
        return [(color, count) for color, count in top_colors.items()]