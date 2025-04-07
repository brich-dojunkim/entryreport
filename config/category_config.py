# config/category_config.py
"""
카테고리 관련 설정을 제공하는 모듈
"""
from .base_config import BaseConfig

class CategoryConfig(BaseConfig):
    """
    카테고리 관련 설정 클래스
    """
    
    # 카테고리 코드-이름 매핑
    CATEGORY_MAPPING = {
        '0001000100080003': '니트/스웨터',
        '0001000100080001': '가디건',
        '0001000100010001': '셔츠/블라우스',
        '0011000700020001': '화장품',
        '0001000100060001': '슬랙스',
        '0001000100060004': '조거/트레이닝',
        '0001000100020002': '티셔츠',
        '0001000100020005': '맨투맨',
        '000100050010': '패션 소품',
        '0001000100070002': '데님 팬츠'
    }
    
    def __init__(self):
        super().__init__()
    
    def get_category_name(self, category_code):
        """
        카테고리 코드에 대한 이름 반환
        
        Parameters:
        - category_code: 카테고리 코드
        
        Returns:
        - 카테고리 이름
        """
        return self.CATEGORY_MAPPING.get(category_code, f"알 수 없는 카테고리 ({category_code})")