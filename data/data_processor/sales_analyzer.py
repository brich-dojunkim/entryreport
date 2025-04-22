# data/data_processor/sales_analyzer.py
import pandas as pd
from config import Config

class SalesAnalyzer:
    """판매 데이터 분석을 담당하는 클래스 (가격, 채널, 베스트셀러 등)"""
    
    def __init__(self, df, config=None):
        """
        Parameters:
        - df: 분석할 데이터프레임
        - config: 설정 객체
        """
        self.df = df
        self.config = config if config is not None else Config()
    
    def get_channel_data(self):
        """판매 채널 분석"""
        if '판매채널' not in self.df.columns:
            return pd.Series(), pd.Series(), 0, [], []
            
        # 채널별 주문 수 계산
        channel_counts = self.df['판매채널'].value_counts()
        
        # 상위 10개 채널 선택
        top_channels = channel_counts.head(10)
        
        # 전체 주문 중 상위 3개 채널의 비율 계산
        top3_channels = channel_counts.head(3)
        top3_ratio = (top3_channels.sum() / channel_counts.sum() * 100).round(1)
        
        # 채널 리스트
        top3_channel_list = top3_channels.index.tolist()
        
        # 데이터 포맷팅
        channel_data = []
        for channel, count in top_channels.items():
            channel_data.append({
                'name': channel,
                'value': count
            })
            
        return channel_counts, top_channels, top3_ratio, top3_channel_list, channel_data
    
    def analyze_price_ranges(self):
        """가격대 분석"""
        if '상품가격' not in self.df.columns:
            return pd.Series(), pd.Series(), []
        
        # 가격대 구간 정의
        price_bins = [0, 10000, 20000, 30000, 50000, 70000, 100000, 150000, 200000, 1000000]
        price_labels = [
            '1만원 미만', '1~2만원', '2~3만원', '3~5만원', 
            '5~7만원', '7~10만원', '10~15만원', '15~20만원', '20만원 이상'
        ]
        
        # 가격대별 상품 수 계산
        price_counts = pd.cut(
            self.df['상품가격'], 
            bins=price_bins, 
            labels=price_labels, 
            right=False
        ).value_counts().sort_index()
        
        # 가격대별 비율 계산
        price_percent = (price_counts / price_counts.sum() * 100).round(1)
        
        # 데이터 포맷팅
        price_data = []
        for price_range, count in price_counts.items():
            percent = price_percent[price_range]
            price_data.append({
                'name': price_range,
                'value': count,
                'percent': percent,
                'range': price_range
            })
        
        return price_counts, price_percent, price_data
    
    def analyze_bestsellers(self):
        """베스트셀러 상품 분석"""
        if '상품명' not in self.df.columns:
            return pd.Series(), []
        
        # 상품별 주문 수 계산
        product_counts = self.df['상품명'].value_counts()
        
        # 상위 10개 상품 선택
        top_products = product_counts.head(10)
        
        # 데이터 포맷팅
        bestseller_data = []
        for idx, (product, count) in enumerate(top_products.items(), 1):
            # 상품명이 너무 길면 잘라서 표시
            display_name = product
            if len(product) > 50:
                display_name = product[:47] + "..."
                
            bestseller_data.append({
                'rank': idx,
                'name': display_name,
                'product': product,
                'count': count,
                'value': count  # 차트 데이터 포맷팅용
            })
        
        return top_products, bestseller_data
    
    def analyze_channel_prices(self):
        """채널별 평균 가격 분석"""
        if '판매채널' not in self.df.columns or '상품가격' not in self.df.columns:
            return {}
            
        # 채널별 평균 가격 계산
        channel_prices = self.df.groupby('판매채널')['상품가격'].mean()
        
        return channel_prices.to_dict()
    
    def analyze_categories(self):
        """카테고리 분석"""
        if '상품 카테고리' not in self.df.columns:
            return pd.Series(), pd.Series(), []
            
        # 카테고리별 주문 수 계산
        category_counts = self.df['상품 카테고리'].value_counts()
        
        # 상위 10개 카테고리 선택
        top_categories = category_counts.head(10)
        
        # 데이터 포맷팅
        category_data = []
        for category, count in top_categories.items():
            category_data.append({
                'name': self.config.get_category_name(category),
                'id': category,
                'value': count
            })
            
        return category_counts, top_categories, category_data