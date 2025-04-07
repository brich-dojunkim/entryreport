# config/keyword_config.py
"""
키워드 관련 설정을 제공하는 모듈
"""
from .base_config import BaseConfig

class KeywordConfig(BaseConfig):
    """
    키워드 추출 관련 설정 클래스
    """
    
    # 불용어 목록 (제외할 단어)
    STOP_WORDS = [
        "1+1", "기획", "특가", "세트", "쿠폰", "할인", "단독", "주문", "폭주", 
        "배송", "당일", "브리치", "[브리치]", "color", "ver", "개", 
        "세트", "택1", "선택", "ver.", "버전", "모음", "컬러", "col",
        "쇼핑몰", "인기", "best", "컬렉션", "쿠폰다운", "%", 
        "주문폭주", "만원", "천장돌파"
    ]
    
    # 비패션 키워드 (필터링 대상)
    NON_FASHION_KEYWORDS = [
        'the', 'and', 'for', 'with', 'by', 'in', 'on', 'at', 'to', 'from', 'of',
        'shop', 'store', 'mall', 'official', 'charge', 'battery', 'fast', 'out', 'way',
        '배송', '구매', '상품', '제품', '구성', '세트', '할인', '특가', '이벤트', '쿠폰',
        '무료', '당일', '빠른', '행사', '선물', '증정', '필수', '사은품', '판매', '출시',
        '매장', '신상', '인기', '베스트', '추천', '기획', '단독', '오픈', '한정', '수량',
        'kg', 'g', 'ml', 'cm', 'm', '개', '팩', '봉', '박스', '묶음', '듀오', '세트'
    ]
    
    # 패션 도메인 관련 단어 패턴
    FASHION_PATTERNS = [
        r'[가-힣]+핏', r'[가-힣]+라인', r'[가-힣]+컷', r'[가-힣]+스타일', 
        r'[가-힣]+소재', r'[가-힣]+패턴', r'[가-힣]+디자인', r'[가-힣]+색상',
        r'[가-힣]+넥', r'[가-힣]+팬츠', r'[가-힣]+티', r'[가-힣]+탑', 
        r'[가-힣]+자켓', r'[가-힣]+코트', r'[가-힣]+원피스'
    ]
    
    # 패션 관련 키워드
    FASHION_KEYWORDS = [
        '티셔츠', '셔츠', '블라우스', '니트', '스웨터', '가디건', '자켓', '코트', '패딩', 
        '바지', '팬츠', '청바지', '데님', '스커트', '레깅스', '원피스', '드레스',
        '슬림핏', '레귤러핏', '오버핏', '박시핏', '와이드', '스트레이트', '크롭',
        '라운드넥', '브이넥', '터틀넥', '카라', '후드', '맨투맨', '민소매', '나시',
        '플리츠', '러플', '프릴', '셔링', '밴딩', '스트라이프', '체크', '도트', '플라워',
        '남성', '여성', '남자', '여자', '키즈', '아동', '주니어', '시즌', '봄', '여름', '가을', '겨울',
        '웨어', '의류', '정장', '캐주얼', '스포티', '빈티지', '오버사이즈', '루즈핏', '슬림',
        '반팔', '긴팔', '7부', '9부', '노카라', '베이직', '클래식', '모던', '빅사이즈', '플러스사이즈',
        '롱', '쇼트', '미니', '미디', '맥시', '골지', '울', '린넨', '면', '코튼', '폴리', '트위드',
        '숄더', '크로스', '백팩', '토트', '클러치', '슬링', '힙색', '지갑', '파우치',
        '스니커즈', '로퍼', '슬리퍼', '부츠', '힐', '플랫', '샌들', '뮬', '운동화'
    ]
    
    def __init__(self):
        super().__init__()
    
    def get_stop_words(self):
        """불용어 목록 반환"""
        return self.get_env_list('BFLOW_EXTRA_STOP_WORDS', self.STOP_WORDS)
    
    def get_non_fashion_keywords(self):
        """비패션 키워드 목록 반환"""
        return self.get_env_list('BFLOW_EXTRA_NON_FASHION_KEYWORDS', self.NON_FASHION_KEYWORDS)
    
    def get_fashion_patterns(self):
        """패션 관련 패턴 목록 반환"""
        return self.get_env_list('BFLOW_EXTRA_FASHION_PATTERNS', self.FASHION_PATTERNS)
    
    def get_fashion_keywords(self):
        """패션 관련 키워드 목록 반환"""
        return self.get_env_list('BFLOW_EXTRA_FASHION_KEYWORDS', self.FASHION_KEYWORDS)