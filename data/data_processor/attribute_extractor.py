# data/data_processor/attribute_extractor.py
import re
from collections import Counter
from config import Config

class AttributeExtractor:
    """상품 속성(키워드, 색상, 사이즈, 소재, 디자인 등) 추출을 담당하는 클래스"""
    
    def __init__(self, df, config=None):
        """
        Parameters:
        - df: 분석할 데이터프레임
        - config: 설정 객체
        """
        self.df = df
        self.config = config if config is not None else Config()
    
    def extract_product_keywords(self):
        """상품명에서 키워드 추출"""
        if '상품명' not in self.df.columns:
            return []
        
        # 불용어 목록 가져오기
        stop_words = self.config.get_stop_words()
        
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
        
        word_counts = Counter(all_words)
        top_keywords = word_counts.most_common(20)
        return top_keywords

    def _extract_option_attribute(self, keywords, top_n=10):
        """옵션정보 컬럼에서 키워드 추출 (공통 함수)"""
        if '옵션정보' not in self.df.columns:
            return []
        extracted = []
        for option in self.df['옵션정보'].dropna().astype(str):
            for keyword in keywords:
                if keyword in option:
                    extracted.append(keyword)
                    break
        return Counter(extracted).most_common(top_n)
    
    def extract_colors(self):
        """옵션정보에서 색상 추출"""
        color_keywords = self.config.get_product_attributes('colors')
        return self._extract_option_attribute(color_keywords, top_n=10)
    
    def extract_sizes(self):
        """옵션정보에서 사이즈 추출 및 FREE 사이즈 비율 계산"""
        size_keywords = self.config.get_product_attributes('sizes')
        # 공통 함수로 사이즈 추출
        extracted = []
        if '옵션정보' in self.df.columns:
            for option in self.df['옵션정보'].dropna().astype(str):
                for size in size_keywords:
                    if size in option:
                        extracted.append(size)
                        break
        size_counts = Counter(extracted)
        top_sizes = size_counts.most_common(10)
        free_size_count = size_counts.get('FREE', 0)
        free_size_ratio = (free_size_count / sum(size_counts.values()) * 100) if size_counts else 0
        
        return top_sizes, free_size_ratio
    
    def _extract_attribute_from_columns(self, columns, keywords, top_n=10):
        """여러 컬럼에서 키워드 추출 (공통 함수)"""
        extracted = []
        for col in columns:
            if col in self.df.columns:
                for text in self.df[col].dropna().astype(str):
                    for keyword in keywords:
                        if keyword in text:
                            extracted.append(keyword)
                            break
        return Counter(extracted).most_common(top_n)
    
    def extract_materials(self):
        """상품명과 상세설명에서 소재 추출"""
        material_keywords = self.config.get_product_attributes('materials')
        return self._extract_attribute_from_columns(['상품명', '상품상세설명'], material_keywords, top_n=10)
    
    def extract_designs(self):
        """상품명과 상세설명에서 디자인 요소 추출"""
        design_keywords = self.config.get_product_attributes('designs')
        return self._extract_attribute_from_columns(['상품명', '상품상세설명'], design_keywords, top_n=10)
