# data/keyword_extractor/tfidf_extractor.py
"""
TF-IDF 기반 키워드 추출 로직
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfExtractor:
    """TF-IDF로 상품 키워드를 추출하는 로직을 담은 클래스/헬퍼 함수 모음"""

    @staticmethod
    def extract_tfidf_keywords(texts, n_keywords=10):
        """
        TF-IDF로 키워드 추출
        Parameters:
        - texts: 전처리된 텍스트의 리스트(pd.Series도 가능)
        - n_keywords: 추출할 키워드 수
        Returns:
        - [(키워드, tfidf값), ...] 형태의 리스트
        """
        if len(texts) == 0:
            return []

        tfidf = TfidfVectorizer(
            max_features=100,
            min_df=5,
            ngram_range=(1, 2)
        )

        try:
            tfidf_matrix = tfidf.fit_transform(texts)
        except ValueError:
            # 데이터가 부족하거나 부적절한 경우
            return []

        feature_names = tfidf.get_feature_names_out()
        tfidf_scores = tfidf_matrix.mean(axis=0).A1

        # 상위 n_keywords 추출
        top_indices = tfidf_scores.argsort()[-n_keywords:][::-1]
        top_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
        return top_keywords
