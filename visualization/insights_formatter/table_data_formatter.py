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
            if 'colors' not in self.insights or 'top_items' not in self.insights['colors']:
                return []
            return [{"name": c, "value": v} for c, v in self.insights['colors']['top_items'][:7]]
        elif data_type == 'prices':
            if 'price_ranges' not in self.insights or 'price_data' not in self.insights['price_ranges']:
                return []
            return self.insights['price_ranges']['price_data']
        elif data_type == 'channels':
            if 'channels' not in self.insights or 'channel_data' not in self.insights['channels']:
                return []
            return self.insights['channels']['channel_data']
        elif data_type == 'sizes':
            if 'sizes' not in self.insights or 'sizes_data' not in self.insights['sizes']:
                return []
            return self.insights['sizes']['sizes_data']
        elif data_type == 'materials':
            if 'materials' not in self.insights or 'materials_data' not in self.insights['materials']:
                return []
            return self.insights['materials']['materials_data']
        elif data_type == 'designs':
            if 'designs' not in self.insights or 'designs_data' not in self.insights['designs']:
                return []
            return self.insights['designs']['designs_data']
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
