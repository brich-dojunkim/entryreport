# config/category_config.py
import pandas as pd
import os
from pathlib import Path
from .base_config import BaseConfig

class CategoryConfig(BaseConfig):
    """
    카테고리 관련 설정 클래스 (CSV 파일에서 로드)
    """
    
    def __init__(self):
        super().__init__()
        # config 폴더 내의 category.csv 파일 경로
        config_dir = Path(__file__).parent
        self.category_file = str(config_dir / 'category.csv')
        self.category_mapping = {}
        self.allowed_categories = set()
        self._load_categories()
    
    def _load_categories(self):
        """CSV 파일에서 카테고리 데이터 로드"""
        try:
            # 파일이 존재하는지 확인
            if not os.path.exists(self.category_file):
                print(f"카테고리 파일을 찾을 수 없습니다: {self.category_file}")
                return
            
            # CSV 파일 읽기
            df = pd.read_csv(self.category_file)
            
            # 모든 카테고리 코드를 허용 목록에 추가
            for _, row in df.iterrows():
                code = str(row['Code'])
                name = row['Name']
                
                # 카테고리 매핑 저장 (두 가지 형식 모두 지원)
                self.category_mapping[code] = name
                # 숫자 형식도 매핑에 추가 (앞의 0을 제거)
                numeric_code = code.lstrip('0')
                if numeric_code:  # 빈 문자열이 아닌 경우에만 추가
                    self.category_mapping[numeric_code] = name
                    self.allowed_categories.add(numeric_code)
                
                # 모든 카테고리를 허용 목록에 추가 (두 가지 형식 모두)
                self.allowed_categories.add(code)
            
            print(f"CSV에서 {len(self.allowed_categories)}개의 카테고리 로드 완료")
            
        except Exception as e:
            print(f"카테고리 데이터 로드 중 오류 발생: {e}")
        
    def get_category_name(self, category_code):
        """카테고리 코드에 대한 이름 반환"""
        if pd.isna(category_code):
            return "알 수 없는 카테고리"
        
        # 숫자형이면 문자열로 변환
        if isinstance(category_code, (int, float)):
            category_code = str(int(category_code))
        else:
            category_code = str(category_code)
        
        # 매핑에서 찾기
        if category_code in self.category_mapping:
            return self.category_mapping[category_code]
        
        # 앞의 0을 제거하고 찾기
        numeric_code = category_code.lstrip('0')
        if numeric_code in self.category_mapping:
            return self.category_mapping[numeric_code]
        
        return f"알 수 없는 카테고리 ({category_code})"
    
    def is_allowed_category(self, category_code):
        """CSV에 정의된 카테고리인지 확인"""
        if pd.isna(category_code):
            return False
        
        # 숫자형이면 문자열로 변환
        if isinstance(category_code, (int, float)):
            category_code = str(int(category_code))
        else:
            category_code = str(category_code)
        
        # 허용 목록에서 찾기
        if category_code in self.allowed_categories:
            return True
        
        # 앞의 0을 제거하고 찾기
        numeric_code = category_code.lstrip('0')
        return numeric_code in self.allowed_categories