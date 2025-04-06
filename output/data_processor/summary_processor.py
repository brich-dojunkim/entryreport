# output/data_processor/summary_processor.py
"""
인사이트 데이터에서 요약 정보를 추출하는 모듈
"""

class SummaryProcessor:
    """
    insights 딕셔너리에서 주요 요약 정보를 추출하는 클래스.
    모든 항목은 리스트의 dict 형식으로 보장합니다.
    """
    def __init__(self, insights):
        self.insights = insights

    def _ensure_dict_list(self, items):
        """
        items가 튜플 리스트이면 dict 리스트로 변환.
        이미 dict 리스트이면 그대로 반환.
        """
        if items and isinstance(items[0], tuple):
            return [{'name': t[0], 'count': t[1], 'value': t[1]} for t in items]
        return items

    def generate_summary(self):
        """
        인사이트 데이터에서 요약 정보를 추출하여 딕셔너리로 반환
        """
        summary = {}
        # product_keywords: 반드시 dict 형태
        if 'product_keywords' in self.insights and isinstance(self.insights['product_keywords'], dict):
            top_keywords = self.insights['product_keywords'].get('top_keywords', [])
            summary['top_keywords'] = self._ensure_dict_list(top_keywords)[:3]
        else:
            summary['top_keywords'] = []
        
        if 'colors' in self.insights:
            if isinstance(self.insights['colors'], dict):
                top_colors = self.insights['colors'].get('top_items', [])
            elif isinstance(self.insights['colors'], list):
                top_colors = self.insights['colors']
            else:
                top_colors = []
            summary['top_colors'] = self._ensure_dict_list(top_colors)[:3]
        
        if 'price_ranges' in self.insights and isinstance(self.insights['price_ranges'], dict):
            price_counts = self.insights['price_ranges'].get('counts', None)
            if price_counts is not None and not price_counts.empty:
                summary['main_price_range'] = price_counts.idxmax()
                summary['main_price_percent'] = self.insights['price_ranges'].get('percent', {}).get(summary['main_price_range'], 0)
        
        if 'channels' in self.insights and isinstance(self.insights['channels'], dict):
            summary['top3_channels'] = self.insights['channels'].get('top3_channels', [])
            summary['top3_ratio'] = self.insights['channels'].get('top3_ratio', 0)
        
        if 'sizes' in self.insights and isinstance(self.insights['sizes'], dict):
            summary['free_size_ratio'] = self.insights['sizes'].get('free_size_ratio', 0)
            summary['top_sizes'] = self._ensure_dict_list(self.insights['sizes'].get('top_items', []))
        
        if 'materials' in self.insights:
            if isinstance(self.insights['materials'], dict):
                materials = self.insights['materials'].get('top_items', [])
            elif isinstance(self.insights['materials'], list):
                materials = self.insights['materials']
            else:
                materials = []
            summary['top_materials'] = [item['name'] if isinstance(item, dict) else item[0] for item in self._ensure_dict_list(materials)][:3]
        
        if 'designs' in self.insights:
            if isinstance(self.insights['designs'], dict):
                designs = self.insights['designs'].get('top_items', [])
            elif isinstance(self.insights['designs'], list):
                designs = self.insights['designs']
            else:
                designs = []
            summary['top_designs'] = [item['name'] if isinstance(item, dict) else item[0] for item in self._ensure_dict_list(designs)][:3]
        
        if 'bestsellers' in self.insights and isinstance(self.insights['bestsellers'], dict):
            summary['total_orders'] = len(self.insights['bestsellers'].get('top_products', {}))
            best_products = self.insights['bestsellers'].get('top_products', {}).items()
            summary['top_products'] = [(product, count) for product, count in best_products][:5]
        
        if 'auto_keywords' in self.insights and isinstance(self.insights['auto_keywords'], dict):
            if 'style_keywords' in self.insights['auto_keywords']:
                summary['auto_style_keywords'] = self._ensure_dict_list(self.insights['auto_keywords']['style_keywords'])[:5]
            if 'additional_product_keywords' in self.insights['auto_keywords']:
                additional = self.insights['auto_keywords']['additional_product_keywords']
                summary['auto_product_keywords'] = self._ensure_dict_list(additional)[:5]
            if 'color_groups' in self.insights['auto_keywords']:
                summary['auto_color_groups'] = self._ensure_dict_list(self.insights['auto_keywords']['color_groups'])[:5]
        
        return summary