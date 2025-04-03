# modules/config.py
"""
비플로우 분석 시스템의 설정 관리 모듈
"""
import os
from pathlib import Path

class Config:
    """
    설정 관리 클래스
    환경 변수 또는 기본값에서 설정을 로드
    """
    
    # 상품 분석 시 제외할 불용어 목록
    STOP_WORDS = [
        "1+1", "기획", "특가", "세트", "쿠폰", "할인", "단독", "주문", "폭주", 
        "배송", "당일", "브리치", "[브리치]", "color", "ver", "개", 
        "세트", "택1", "선택", "ver.", "버전", "모음", "컬러", "col",
        "쇼핑몰", "인기", "best", "컬렉션", "쿠폰다운", "%", 
        "주문폭주", "만원", "천장돌파"
    ]
    
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
            '체크', '스트라이프', '도트', '플라워', '플로랄', '지브라', '레오파드', 
            '카모', '타이다이', '그라데이션', '프린트', '패치', '자수', '레터링', 
            '로고', '아가일', '기하학', '페이즐리'
        ]
    }
    
    # 차트 관련 설정
    CHART_COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']
    
    # 기본 설정값
    DEFAULT_OUTPUT_FOLDER = 'bflow_reports'
    DEFAULT_DASHBOARD_PORT = 8050
    DEFAULT_REPORT_PORT = 8051
    DEFAULT_TEMPLATE_FOLDER = 'templates'
    
    def __init__(self):
        """환경 변수 또는 기본값으로 설정 초기화"""
        # 출력 폴더 설정
        self.output_folder = os.environ.get('BFLOW_OUTPUT_FOLDER', self.DEFAULT_OUTPUT_FOLDER)
        
        # 포트 번호 설정
        try:
            self.dashboard_port = int(os.environ.get('BFLOW_DASHBOARD_PORT', self.DEFAULT_DASHBOARD_PORT))
        except (ValueError, TypeError):
            self.dashboard_port = self.DEFAULT_DASHBOARD_PORT
            
        try:
            self.report_port = int(os.environ.get('BFLOW_REPORT_PORT', self.DEFAULT_REPORT_PORT))
        except (ValueError, TypeError):
            self.report_port = self.DEFAULT_REPORT_PORT
        
        # 템플릿 폴더
        self.template_folder = Path(os.environ.get('BFLOW_TEMPLATE_FOLDER', self.DEFAULT_TEMPLATE_FOLDER))
    
    def get_stop_words(self):
        """불용어 목록 반환"""
        # 환경 변수로 추가 불용어 설정 가능
        extra_stop_words = os.environ.get('BFLOW_EXTRA_STOP_WORDS', '')
        if extra_stop_words:
            return self.STOP_WORDS + extra_stop_words.split(',')
        return self.STOP_WORDS
    
    def get_chart_colors(self):
        """차트 색상 목록 반환"""
        return self.CHART_COLORS
    
    def get_product_attributes(self, attr_type=None):
        """제품 속성 키워드 반환"""
        if attr_type and attr_type in self.PRODUCT_ATTRIBUTES:
            return self.PRODUCT_ATTRIBUTES[attr_type]
        return self.PRODUCT_ATTRIBUTES
    
    def get_category_name(self, category_code):
        """카테고리 코드에 대한 이름 반환"""
        return self.CATEGORY_MAPPING.get(category_code, f"알 수 없는 카테고리 ({category_code})")
    
    def create_output_folders(self):
        """필요한 출력 폴더 생성"""
        # 기본 출력 폴더
        output_path = Path(self.output_folder)
        output_path.mkdir(exist_ok=True)
        
        # 차트 폴더
        charts_path = output_path / 'charts'
        charts_path.mkdir(exist_ok=True)
        
        return output_path