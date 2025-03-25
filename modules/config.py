# modules/config.py
"""
비플로우 분석 시스템의 설정 상수들을 관리하는 모듈
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

# 출력 관련 설정
DEFAULT_OUTPUT_FOLDER = 'bflow_reports'
DEFAULT_DASHBOARD_PORT = 8050