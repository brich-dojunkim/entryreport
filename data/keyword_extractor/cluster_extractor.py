"""
클러스터링(스타일 키워드) 추출 로직
"""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

class ClusterExtractor:
    """K-Means 등 클러스터링을 통해 스타일 키워드를 자동 추출"""

    @staticmethod
    def extract_cluster_keywords(texts, n_clusters=5, n_keywords=3):
        """
        클러스터링을 통한 키워드 추출
        Parameters:
        - texts: 전처리된 텍스트 리스트
        - n_clusters: 클러스터 개수
        - n_keywords: 각 클러스터에서 추출할 키워드 수
        Returns:
        - 키워드 문자열들의 리스트 (ex: ["basic", "fit", "cotton", ...])
        """
        if len(texts) < n_clusters:
            return []

        try:
            count_vec = CountVectorizer(max_features=200, min_df=3)
            term_matrix = count_vec.fit_transform(texts)

            # 특성이 너무 적으면 클러스터링 불가
            if term_matrix.shape[1] < 5:
                return []

            kmeans = KMeans(n_clusters=min(n_clusters, len(texts) // 5 + 1), random_state=42)
            clusters = kmeans.fit_predict(term_matrix)

            feature_names = count_vec.get_feature_names_out()
            style_keywords = []

            for i in range(kmeans.n_clusters):
                # 해당 클러스터 문서 인덱스
                cluster_doc_indices = np.where(clusters == i)[0]
                if len(cluster_doc_indices) > 0:
                    # 클러스터 내 문서들의 단어 빈도 합계
                    cluster_term_freq = term_matrix[cluster_doc_indices].sum(axis=0).A1
                    top_indices = cluster_term_freq.argsort()[-n_keywords:][::-1]
                    cluster_keywords = [feature_names[idx] for idx in top_indices]
                    style_keywords.append(cluster_keywords)

            # 2차원 리스트를 1차원으로 펴기
            flattened_keywords = [kw for cluster in style_keywords for kw in cluster]
            return flattened_keywords
        except Exception as e:
            print(f"클러스터링 중 오류 발생: {e}")
            return []
