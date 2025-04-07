# config/product_config.py
"""
제품 속성 관련 설정을 제공하는 모듈
"""
from .base_config import BaseConfig

class ProductConfig(BaseConfig):
    """
    제품 속성 관련 설정 클래스
    """
    
    # 제품 속성 키워드 사전 정의
    PRODUCT_ATTRIBUTES = {
        'colors': [
            '블랙', '화이트', '아이보리', '베이지', '그레이', '차콜', '네이비', 
            '핑크', '블루', '퍼플', '레드', '그린', '옐로우', '오렌지', '브라운', 
            '카키', '와인', '연청', '중청', '진청'
        ],
        'sizes': ['FREE', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '55', '66', '77', '88', '95', '100', '105', '110'],
        'materials': [
            '면', '코튼', '니트', '데님', '린넨', '레이온', '폴리', '울', '캐시미어', 
            '쉬폰', '레더', '스웨이드', '퍼', '벨벳', '실크', '레이스', '퀼팅', '트위드', 
            '폴리에스테르', '텐셀', '모달', '스판', '와플', '자수', '시스루'
        ],
        'designs': [
            '체크', '스트라이프', '도트', '플라워', '플로럴', '지브라', '레오파드', 
            '카모', '타이다이', '그라데이션', '프린트', '패치', '자수', '레터링', 
            '로고', '아가일', '기하학', '페이즐리'
        ]
    }
    
    def __init__(self):
        super().__init__()
    
    def get_attribute(self, attr_type=None):
        """
        제품 속성 반환
        
        Parameters:
        - attr_type: 속성 타입 (colors, sizes, materials, designs)
        
        Returns:
        - 해당 속성 목록 또는 전체 속성 사전
        """
        if attr_type and attr_type in self.PRODUCT_ATTRIBUTES:
            # 환경 변수에서 추가 속성 확인
            env_var = f'BFLOW_EXTRA_{attr_type.upper()}'
            extra_values = self.get_env_list(env_var)
            
            if extra_values:
                return self.PRODUCT_ATTRIBUTES[attr_type] + extra_values
            return self.PRODUCT_ATTRIBUTES[attr_type]
        
        return self.PRODUCT_ATTRIBUTES