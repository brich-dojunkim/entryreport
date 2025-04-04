# output/report_generator/data_processor/data_processor.py
"""
리포트용 데이터 처리 모듈
템플릿 변수 준비 및 데이터 통합 담당
"""
from datetime import datetime

from output.report_generator.data_processor.strategy_processor import StrategyProcessor
from output.report_generator.data_processor.auto_keyword_processor import AutoKeywordProcessor

class ReportDataProcessor:
    """리포트 데이터 통합 처리 클래스"""
    
    def __init__(self, insights, formatter):
        """
        데이터 처리기 초기화
        
        Parameters:
        - insights: 분석 결과 딕셔너리
        - formatter: InsightsFormatter 인스턴스
        """
        self.insights = insights
        self.formatter = formatter
        
        # 전략/자동 키워드 등 세부 프로세서
        self.strategy_processor = StrategyProcessor(formatter)
        self.auto_keyword_processor = AutoKeywordProcessor()
    
    def prepare_template_variables(self, now, summary):
        """
        템플릿 변수 준비 및 통합
        
        Parameters:
        - now: 현재 시각 (datetime)
        - summary: BaseGenerator에서 추출해둔 요약 정보
        
        Returns:
        - 템플릿에 전달할 변수 딕셔너리
        """
        template_vars = {
            'title': '엔트리 셀러 인사이트 리포트',
            'timestamp': now.strftime('%Y년 %m월 %d일 %H:%M'),
            'period': f"{self.insights.get('start_date', '알 수 없음')} ~ {self.insights.get('end_date', '알 수 없음')}",
            'total_orders': len(self.insights.get('df', [])) if 'df' in self.insights else summary.get('total_orders', 0),
            'current_year': datetime.now().year
        }

        # 1) 요약 정보
        template_vars.update(self._prepare_summary_variables(summary))

        # 2) 분석 정보
        template_vars.update(self._prepare_analysis_variables(summary))

        # 3) 전략 (strategy_processor)
        template_vars.update(self.strategy_processor.prepare_strategy_variables(self.insights, summary))

        # 4) 자동 키워드 (auto_keyword_processor)
        template_vars.update(self.auto_keyword_processor.prepare_auto_keywords_variables(self.insights))
        
        return template_vars
    
    def _prepare_summary_variables(self, summary):
        """
        요약 정보 변수 준비 (기존 _prepare_summary_variables 로직)
        """
        # 상품군 정보
        if 'top_keywords' in summary and len(summary['top_keywords']) >= 3:
            kw = summary['top_keywords']
            product_insight = f"{kw[0]['name']}({kw[0]['count']}건), {kw[1]['name']}({kw[1]['count']}건), {kw[2]['name']}({kw[2]['count']}건)"
            product_keywords = ', '.join([item['name'] for item in kw[:3]])
        else:
            product_insight = "데이터 부족"
            product_keywords = "데이터 부족"

        # 가격대 정보
        if 'main_price_range' in summary and 'main_price_percent' in summary:
            price_insight = f"{summary['main_price_range']} 상품이 전체의 {summary['main_price_percent']:.1f}%"
            price_range = summary['main_price_range']
        else:
            price_insight = "데이터 부족"
            price_range = "데이터 부족"

        # 판매채널 정보
        if 'top3_channels' in summary and summary['top3_channels']:
            channel_insight = f"{', '.join(summary['top3_channels'])} (전체 주문의 {summary.get('top3_ratio', 0):.1f}%)"
            channels = ', '.join(summary['top3_channels'][:3])
        else:
            channel_insight = "데이터 부족"
            channels = "데이터 부족"

        # 색상 정보
        if 'top_colors' in summary and len(summary['top_colors']) >= 3:
            c1 = summary['top_colors'][0]
            c2 = summary['top_colors'][1]
            c3 = summary['top_colors'][2]
            color_insight = f"{c1['name']}({c1['count']}건), {c2['name']}({c2['count']}건), {c3['name']}({c3['count']}건)"
            colors = ', '.join([item['name'] for item in summary['top_colors'][:3]])
        else:
            color_insight = "데이터 부족"
            colors = "데이터 부족"

        # 사이즈 정보
        if 'free_size_ratio' in summary:
            size_insight = f"FREE 사이즈가 전체의 {summary['free_size_ratio']:.1f}%"
        else:
            size_insight = "데이터 부족"

        return {
            'product_insight': product_insight,
            'product_keywords': product_keywords,
            'price_insight': price_insight,
            'price_range': price_range,
            'channel_insight': channel_insight,
            'channels': channels,
            'color_insight': color_insight,
            'colors': colors,
            'size_insight': size_insight
        }
    
    def _prepare_analysis_variables(self, summary):
        """
        분석 정보 변수 준비 (기존 _prepare_analysis_variables 로직)
        """
        analysis_vars = {}
        
        # 상품 유형 분석
        analysis_vars['product_keywords_data'] = self._prepare_section_data('product_keywords', 'top_keywords')
        
        # 색상 분석
        analysis_vars['colors_data'] = self._prepare_section_data('colors', 'top_items')
        
        # 가격대 분석
        if 'price_ranges' in self.insights and 'counts' in self.insights['price_ranges']:
            price_counts = self.insights['price_ranges']['counts']
            price_percent = self.insights['price_ranges']['percent']

            if not price_counts.empty:
                price_data = []
                for range_name, count in price_counts.items():
                    pct = price_percent[range_name]
                    price_data.append({
                        'range': range_name,
                        'count': count,
                        'percent': pct
                    })
                analysis_vars['price_data'] = price_data
            else:
                analysis_vars['price_data'] = []
        else:
            analysis_vars['price_data'] = []

        # 판매 채널 분석
        if 'channels' in self.insights and 'top_channels' in self.insights['channels']:
            top_channels = self.insights['channels']['top_channels']
            if not top_channels.empty:
                channel_data = []
                for channel, count in top_channels.items():
                    channel_data.append({
                        'channel': channel,
                        'count': count
                    })
                analysis_vars['channel_data'] = channel_data
            else:
                analysis_vars['channel_data'] = []
        else:
            analysis_vars['channel_data'] = []

        # 채널별 평균 가격
        if 'channel_prices' in self.insights:
            channel_prices = self.insights['channel_prices']
            channel_price_data = []
            for channel, price in channel_prices.items():
                channel_price_data.append({
                    'channel': channel,
                    'price': f"{price:,}원"
                })
            analysis_vars['channel_price_data'] = channel_price_data
        else:
            analysis_vars['channel_price_data'] = []

        # 사이즈 분석
        analysis_vars['sizes_data'] = self._prepare_section_data('sizes', 'top_items')
        
        # 소재 분석
        analysis_vars['materials_data'] = self._prepare_section_data('materials', 'top_items', limit=5)
        
        # 디자인 분석
        analysis_vars['designs_data'] = self._prepare_section_data('designs', 'top_items', limit=5)
        
        # 베스트셀러 분석
        if 'bestsellers' in self.insights and 'top_products' in self.insights['bestsellers']:
            top_products = self.insights['bestsellers']['top_products']
            if not top_products.empty:
                bestseller_data = []
                for idx, (product, count) in enumerate(top_products.items(), 1):
                    if idx > 10:
                        break
                    bestseller_data.append({
                        'rank': idx,
                        'product': product,
                        'count': count
                    })
                analysis_vars['bestseller_data'] = bestseller_data

                # 상위 3개 상품 인사이트
                top3_bestsellers = []
                for idx, (product, count) in enumerate(top_products.items(), 1):
                    if idx > 3:
                        break
                    top3_bestsellers.append({
                        'rank': idx,
                        'product': product,
                        'count': count
                    })
                analysis_vars['top3_bestsellers'] = top3_bestsellers
            else:
                analysis_vars['bestseller_data'] = []
                analysis_vars['top3_bestsellers'] = []
        else:
            analysis_vars['bestseller_data'] = []
            analysis_vars['top3_bestsellers'] = []

        # 인사이트 텍스트 (formatter가 있다면)
        for section in ['product', 'color', 'price', 'channel', 'size', 'material_design']:
            if self.formatter:
                analysis_vars[f'{section}_insight'] = self.formatter.generate_insight_text(section)
            else:
                analysis_vars[f'{section}_insight'] = ""

        return analysis_vars
    
    def _prepare_section_data(self, insights_key, items_key, limit=10):
        """
        섹션 데이터 준비 (공용 메소드)
        """
        if insights_key not in self.insights or items_key not in self.insights[insights_key]:
            return []

        items = self.insights[insights_key][items_key]
        if not items:
            return []

        section_data = []
        if isinstance(items, dict):
            # 딕셔너리(Series 등)
            for item, count in list(items.items())[:limit]:
                section_data.append({
                    'name': item,
                    'count': count
                })
        else:
            # 리스트(튜플) 등
            for item, count in items[:limit]:
                section_data.append({
                    'name': item,
                    'count': count
                })

        return section_data
