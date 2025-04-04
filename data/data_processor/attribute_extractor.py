# data/attribute_extractor.py
import re
from collections import Counter
from config.config import Config

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
            return [], 0
        
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