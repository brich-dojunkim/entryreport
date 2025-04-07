import re
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import clean_text

class TfidfExtractor:
    """TF-IDF로 상품 키워드를 추출하는 로직을 담은 클래스/헬퍼 함수 모음"""

    @staticmethod
    def extract_tfidf_keywords(texts, n_keywords=10):
        """
        TF-IDF로 키워드 추출
        Parameters:
        - texts: 전처리된 텍스트의 리스트 (pd.Series도 가능)
        - n_keywords: 추출할 키워드 수
        Returns:
        - [(키워드, tfidf값), ...] 형태의 리스트
        """
        if len(texts) == 0:
            return []

        tfidf = TfidfVectorizer(
            max_features=100,
            min_df=2,
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
        
        # 필터링: 2글자 이상의 의미있는 단어만 선택
        filtered_keywords = [(kw, score) for kw, score in top_keywords 
                           if len(kw) >= 2 and re.match(r'^[\w가-힣]+$', kw)]
        
        return filtered_keywords
    
    @staticmethod
    def extract_category_tfidf_keywords(df, category_col, text_col, n_keywords=10):
        """
        카테고리별 TF-IDF 키워드 추출
        Parameters:
        - df: 데이터프레임
        - category_col: 카테고리 컬럼명
        - text_col: 텍스트 컬럼명
        - n_keywords: 각 카테고리별 추출할 키워드 수
        Returns:
        - [(키워드, tfidf값), ...] 형태의 통합 리스트
        """
        if category_col not in df.columns or text_col not in df.columns:
            return []
        
        keywords_by_category = {}
        
        # 각 카테고리별 그룹 처리
        for category, group in df.groupby(category_col):
            # 데이터가 충분한 카테고리만 처리
            if len(group) < 5:
                continue
                
            # 전처리: 각 텍스트에 대해 utils의 clean_text 함수를 사용하여 전처리 수행
            texts = [clean_text(text) for text in group[text_col].dropna().astype(str)]
            
            try:
                tfidf = TfidfVectorizer(
                    max_features=50,
                    min_df=2,
                    ngram_range=(1, 2)
                )
                tfidf_matrix = tfidf.fit_transform(texts)
                feature_names = tfidf.get_feature_names_out()
                tfidf_scores = tfidf_matrix.mean(axis=0).A1
                
                # 상위 키워드 추출
                top_indices = tfidf_scores.argsort()[-n_keywords:][::-1]
                cat_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
                
                # 필터링
                filtered_keywords = [(kw, score) for kw, score in cat_keywords 
                                   if len(kw) >= 2 and re.match(r'^[\w가-힣]+$', kw)]
                
                keywords_by_category[category] = filtered_keywords
            except Exception as e:
                print(f"카테고리 '{category}' 키워드 추출 중 오류: {e}")
        
        # 모든 카테고리 키워드 통합
        all_keywords = {}
        for cat_keywords in keywords_by_category.values():
            for kw, score in cat_keywords:
                all_keywords[kw] = all_keywords.get(kw, 0) + score
        
        # 점수순 정렬 후 상위 n_keywords 반환
        return sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:n_keywords]
