# visualization/insights_formatter/table_data_formatter.py
class TableDataFormatter:
    """
    insights 데이터를 테이블이나 차트에 맞게 포맷팅하는 클래스
    """
    def __init__(self, insights):
        self.insights = insights

    def format_data(self, data_type):
        if data_type == 'keywords':
            if 'product_keywords' not in self.insights or 'top_keywords' not in self.insights['product_keywords']:
                return []
            return [{"name": k, "value": v} for k, v in self.insights['product_keywords']['top_keywords'][:10]]
        elif data_type == 'colors':
            if 'colors' not in self.insights:
                return []
            
            # colors는 formatted가 있을 수 있음
            if isinstance(self.insights['colors'], dict) and 'formatted' in self.insights['colors']:
                return self.insights['colors']['formatted']
            # 또는 colors 자체가 리스트일 수 있음
            elif isinstance(self.insights['colors'], list):
                return self.insights['colors']
            return []
        elif data_type == 'prices':
            if 'price_ranges' not in self.insights or 'price_data' not in self.insights['price_ranges']:
                return []
            return self.insights['price_ranges']['price_data']
        elif data_type == 'channels':
            if 'channels' not in self.insights or 'channel_data' not in self.insights['channels']:
                return []
            return self.insights['channels']['channel_data']
        elif data_type == 'sizes':
            if 'sizes' not in self.insights:
                return []
            
            # sizes는 formatted가 있을 수 있음
            if isinstance(self.insights['sizes'], dict) and 'formatted' in self.insights['sizes']:
                return self.insights['sizes']['formatted']
            return []
        elif data_type == 'materials':
            if 'materials' not in self.insights:
                return []
            
            # materials는 formatted가 있을 수 있음
            if isinstance(self.insights['materials'], dict) and 'formatted' in self.insights['materials']:
                return self.insights['materials']['formatted']
            # 또는 materials 자체가 리스트일 수 있음
            elif isinstance(self.insights['materials'], list):
                return self.insights['materials']
            return []
        elif data_type == 'designs':
            if 'designs' not in self.insights:
                return []
            
            # designs는 formatted가 있을 수 있음
            if isinstance(self.insights['designs'], dict) and 'formatted' in self.insights['designs']:
                return self.insights['designs']['formatted']
            # 또는 designs 자체가 리스트일 수 있음
            elif isinstance(self.insights['designs'], list):
                return self.insights['designs']
            return []
        elif data_type == 'bestsellers':
            if 'bestsellers' not in self.insights or 'bestseller_data' not in self.insights['bestsellers']:
                return []
            return self.insights['bestsellers']['bestseller_data']
        elif data_type == 'auto_keywords':
            if 'auto_keywords' not in self.insights:
                return []
            if 'style_keywords' in self.insights['auto_keywords']:
                return [{"name": kw, "value": i+1} for i, kw in enumerate(self.insights['auto_keywords']['style_keywords'][:10])]
            return []
        return []