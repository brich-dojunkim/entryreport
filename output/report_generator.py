from pathlib import Path
from datetime import datetime
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from visualization.chart_generator import ChartGenerator
from visualization.insights_formatter import InsightsFormatter
from output.base_generator import BaseGenerator
from flask import Flask, render_template
import threading
import webbrowser
import time

class ReportGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 HTML 리포트 생성"""
    
    def __init__(self, insights, formatter=None, output_folder='bflow_reports'):
        """
        리포트 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - formatter: InsightsFormatter 인스턴스 (None이면 자동 생성)
        - output_folder: 결과물 저장 폴더
        """
        super().__init__(insights, formatter, output_folder)
        
        # 차트 저장 폴더 생성 (리포트 전용)
        self.chart_folder = self.output_folder / 'charts'
        self.chart_folder.mkdir(exist_ok=True)
        
        # 템플릿 폴더 설정
        self.template_folder = Path('templates')
    
    def generate_html_report(self):
        """
        HTML 리포트 생성
        
        Returns:
        - 생성된 HTML 리포트 파일 경로
        """
        print("HTML 리포트 생성 중...")
        
        # HTML 파일 경로 설정
        html_file = self.output_folder / f"bflow_report_{self.timestamp}.html"
        
        try:
            # 템플릿 변수 준비
            template_vars = self._prepare_template_variables()
            
            # Jinja2 환경 설정
            env = Environment(loader=FileSystemLoader(self.template_folder))
            template = env.get_template('report_template.html')
            
            # 템플릿 렌더링
            output = template.render(**template_vars)
            
            # HTML 파일 저장
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(output)
            
            print(f"HTML 리포트가 생성되었습니다: {html_file}")
            return html_file
            
        except Exception as e:
            print(f"HTML 리포트 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def generate_web_report(self, port=8051, open_browser=True):
        """
        웹 서버를 사용하여 인터랙티브 HTML 리포트 생성
        
        Parameters:
        - port: 웹 서버 포트 번호
        - open_browser: 브라우저 자동 실행 여부 (main.py에서 처리하므로 무시됨)
        
        Returns:
        - 생성된 웹 서버 URL
        """
        print(f"웹 리포트 서버 시작 중... (포트: {port})")
        
        # 템플릿 변수 준비
        template_vars = self._prepare_template_variables()
        
        # Flask 앱 생성
        app = Flask(__name__, 
                   template_folder=str(self.template_folder),
                   static_folder=str(self.output_folder / 'charts'))
        
        # 라우트 설정
        @app.route('/')
        def index():
            return render_template('report_template.html', **template_vars)
        
        # 웹 서버 실행
        try:
            app.run(host='127.0.0.1', port=port, debug=False)
        except Exception as e:
            print(f"웹 리포트 서버 실행 중 오류 발생: {e}")
        
        return f'http://127.0.0.1:{port}'
    
    def _prepare_template_variables(self):
        """
        템플릿 변수 준비
        
        Returns:
        - 템플릿 변수 딕셔너리
        """
        # 기본 정보
        template_vars = {
            'title': '엔트리 셀러 인사이트 리포트',
            'timestamp': self.now.strftime('%Y년 %m월 %d일 %H:%M'),
            'period': f"{self.insights.get('start_date', '알 수 없음')} ~ {self.insights.get('end_date', '알 수 없음')}",
            'total_orders': len(self.insights.get('df', [])) if 'df' in self.insights else self.summary.get('total_orders', 0),
            'current_year': datetime.now().year
        }
        
        # 요약 정보
        template_vars.update(self._prepare_summary_variables())
        
        # 상품 분석 정보
        template_vars.update(self._prepare_analysis_variables())
        
        # 전략 추천 정보
        template_vars.update(self._prepare_strategy_variables())
        
        # 자동 키워드 정보
        template_vars.update(self._prepare_auto_keywords_variables())
        
        return template_vars
    
    def _prepare_summary_variables(self):
        """요약 정보 변수 준비"""
        summary_vars = {}
        
        # 상품군 정보
        if 'top_keywords' in self.summary and len(self.summary['top_keywords']) >= 3:
            kw = self.summary['top_keywords']
            product_insight = f"{kw[0][0]}({kw[0][1]}건), {kw[1][0]}({kw[1][1]}건), {kw[2][0]}({kw[2][1]}건)"
            product_keywords = ', '.join([k[0] for k in kw[:3]])
        else:
            product_insight = "데이터 부족"
            product_keywords = "데이터 부족"
        
        summary_vars['product_insight'] = product_insight
        summary_vars['product_keywords'] = product_keywords
        
        # 가격대 정보
        if 'main_price_range' in self.summary and 'main_price_percent' in self.summary:
            price_insight = f"{self.summary['main_price_range']} 상품이 전체의 {self.summary['main_price_percent']:.1f}%"
            price_range = self.summary['main_price_range']
        else:
            price_insight = "데이터 부족"
            price_range = "데이터 부족"
        
        summary_vars['price_insight'] = price_insight
        summary_vars['price_range'] = price_range
        
        # 판매채널 정보
        if 'top3_channels' in self.summary and self.summary['top3_channels']:
            channel_insight = f"{', '.join(self.summary['top3_channels'])} (전체 주문의 {self.summary.get('top3_ratio', 0):.1f}%)"
            channels = ', '.join(self.summary['top3_channels'][:3])
        else:
            channel_insight = "데이터 부족"
            channels = "데이터 부족"
        
        summary_vars['channel_insight'] = channel_insight
        summary_vars['channels'] = channels
        
        # 색상 정보
        if 'top_colors' in self.summary and len(self.summary['top_colors']) >= 3:
            color_insight = f"{self.summary['top_colors'][0][0]}({self.summary['top_colors'][0][1]}건), " + \
                           f"{self.summary['top_colors'][1][0]}({self.summary['top_colors'][1][1]}건), " + \
                           f"{self.summary['top_colors'][2][0]}({self.summary['top_colors'][2][1]}건)"
            colors = ', '.join([c[0] for c in self.summary['top_colors'][:3]])
        else:
            color_insight = "데이터 부족"
            colors = "데이터 부족"
        
        summary_vars['color_insight'] = color_insight
        summary_vars['colors'] = colors
        
        # 사이즈 정보
        if 'free_size_ratio' in self.summary:
            size_insight = f"FREE 사이즈가 전체의 {self.summary['free_size_ratio']:.1f}%"
        else:
            size_insight = "데이터 부족"
        
        summary_vars['size_insight'] = size_insight
        
        return summary_vars
    
    def _prepare_analysis_variables(self):
        """분석 정보 변수 준비"""
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
                    percent = price_percent[range_name]
                    price_data.append({
                        'range': range_name,
                        'count': count,
                        'percent': percent
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
                    if idx > 10:  # 상위 10개만 표시
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
                    if idx > 3:  # 상위 3개만 상세 분석
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
        
        # 인사이트 텍스트 추가
        for section in ['product', 'color', 'price', 'channel', 'size', 'material_design']:
            analysis_vars[f'{section}_insight'] = self.formatter.generate_insight_text(section)
        
        return analysis_vars
    
    def _prepare_section_data(self, insights_key, items_key, limit=10):
        """섹션 데이터 준비 (통합 메소드)"""
        if insights_key not in self.insights or items_key not in self.insights[insights_key]:
            return []
        
        items = self.insights[insights_key][items_key]
        
        if not items or (isinstance(items, list) and len(items) == 0):
            return []
        
        section_data = []
        
        if isinstance(items, dict):
            # 딕셔너리인 경우 (Series 등)
            for item, count in list(items.items())[:limit]:
                section_data.append({
                    'name': item,
                    'count': count
                })
        else:
            # 리스트인 경우 (리스트 튜플 등)
            for item, count in items[:limit]:
                section_data.append({
                    'name': item,
                    'count': count
                })
        
        return section_data
    
    def _prepare_strategy_variables(self):
        """전략 추천 변수 준비"""
        strategy_vars = {}
        
        # 실행 가이드 생성
        guide = self.formatter.get_execution_guide()
        
        if not guide:
            strategy_vars['has_strategy'] = False
            return strategy_vars
        
        strategy_vars['has_strategy'] = True
        
        # 키워드 추출
        keywords = [kw for kw, _ in self.summary.get('top_keywords', [])[:3]]
        colors = [color for color, _ in guide.get('top_colors', [])[:3]]
        materials = guide.get('material_keywords', [])
        designs = guide.get('design_keywords', [])
        
        # 자동 추출 스타일 키워드
        auto_style_keywords = guide.get('auto_style_keywords', [])
        
        # 자동 추출 상품 키워드
        auto_product_keywords = guide.get('auto_product_keywords', [])
        
        # 추천 정보 추가
        if auto_product_keywords:
            strategy_vars['product_keywords'] = ', '.join(auto_product_keywords)
        else:
            strategy_vars['product_keywords'] = ', '.join(keywords) if keywords else '데이터 없음'
            
        strategy_vars['colors'] = ', '.join([c for c in colors]) if colors else '데이터 없음'
        strategy_vars['materials'] = ', '.join(materials) if materials else '데이터 없음'
        strategy_vars['designs'] = ', '.join(designs) if designs else '데이터 없음'
        
        # 자동 추출 키워드
        strategy_vars['has_auto_keywords'] = bool(auto_style_keywords)
        strategy_vars['auto_style_keywords'] = ', '.join(auto_style_keywords[:5]) if auto_style_keywords else ''
        
        # 가격 및 채널 전략
        strategy_vars['main_price_range'] = guide.get('main_price_range', '데이터 없음')
        strategy_vars['main_price_percent'] = guide.get('main_price_percent', 0)
        
        channels = guide.get('channels', [])
        strategy_vars['has_channels'] = len(channels) >= 2
        strategy_vars['top_channels'] = ', '.join(channels[:2]) if channels and len(channels) >= 2 else '데이터 없음'
        
        # 종합 전략 요약
        strategy_summary = []
        
        if keywords and colors:
            strategy_summary.append({
                'point': f"{keywords[0]} 카테고리에 {colors[0]} 컬러로 진입"
            })
        
        if 'main_price_range' in guide:
            strategy_summary.append({
                'point': f"{guide['main_price_range']} 가격대에 집중"
            })
        
        if channels:
            strategy_summary.append({
                'point': f"{channels[0]} 채널을 우선적으로 공략"
            })
        
        if materials and designs:
            strategy_summary.append({
                'point': f"{materials[0]} 소재와 {designs[0]} 디자인 요소를 활용한 상품 개발"
            })
        
        if auto_style_keywords and len(auto_style_keywords) > 0:
            strategy_summary.append({
                'point': f"{auto_style_keywords[0]} 스타일 키워드를 상품명과 설명에 활용"
            })
        elif 'free_size_ratio' in guide:
            strategy_summary.append({
                'point': f"사이즈는 FREE 중심으로 구성 (전체의 {guide['free_size_ratio']:.1f}%)"
            })
        
        strategy_vars['strategy_summary'] = strategy_summary
        
        # 추천 상품 목록
        if guide.get('recommended_products'):
            recommended_products = []
            for idx, product in enumerate(guide['recommended_products'][:3], 1):
                recommended_products.append({
                    'index': idx,
                    'name': product
                })
            strategy_vars['recommended_products'] = recommended_products
            strategy_vars['has_recommended_products'] = True
        else:
            strategy_vars['recommended_products'] = []
            strategy_vars['has_recommended_products'] = False
        
        return strategy_vars
    
    def _prepare_auto_keywords_variables(self):
        """자동 추출 키워드 변수 준비"""
        auto_vars = {}
        
        # 데이터 없는 경우 처리
        if 'auto_keywords' not in self.insights:
            auto_vars['has_auto_keywords'] = False
            return auto_vars
        
        auto_vars['has_auto_keywords'] = True
        
        # 스타일 키워드
        if 'style_keywords' in self.insights['auto_keywords']:
            style_keywords = self.insights['auto_keywords']['style_keywords']
            
            if style_keywords:
                auto_vars['style_keywords'] = style_keywords[:10]
                auto_vars['has_style_keywords'] = True
            else:
                auto_vars['has_style_keywords'] = False
        else:
            auto_vars['has_style_keywords'] = False
        
        # 상품 키워드
        if 'additional_product_keywords' in self.insights['auto_keywords']:
            product_keywords = self.insights['auto_keywords']['additional_product_keywords']
            
            if product_keywords:
                # 자동 추출 키워드 포맷팅
                auto_vars['product_keywords'] = [{"keyword": kw, "score": float(score)} for kw, score in product_keywords[:8]]
                auto_vars['has_product_keywords'] = True
                
                # 가이드에 전달할 자동 추출 키워드 리스트 (문자열만)
                auto_product_keywords = [kw for kw, _ in product_keywords[:8]]
                auto_vars['auto_product_keywords'] = auto_product_keywords
            else:
                auto_vars['has_product_keywords'] = False
        else:
            auto_vars['has_product_keywords'] = False
        
        # 색상 그룹
        if 'color_groups' in self.insights['auto_keywords']:
            color_groups = self.insights['auto_keywords']['color_groups']
            
            if color_groups:
                auto_vars['color_groups'] = [{'color': color, 'count': float(count) if hasattr(count, 'item') else count} for color, count in color_groups[:8]]
                auto_vars['has_color_groups'] = True
            else:
                auto_vars['has_color_groups'] = False
        else:
            auto_vars['has_color_groups'] = False
        
        # 인사이트 텍스트
        auto_insights = []
        
        if auto_vars.get('has_style_keywords', False):
            auto_insights.append({
                'text': f"AI가 분석한 주요 스타일 키워드는 **{', '.join(style_keywords[:3])}**입니다."
            })
            auto_insights.append({
                'text': "이 스타일 키워드를 상품명과 상세 설명에 활용하여 검색 노출을 높일 수 있습니다."
            })
        
        if auto_vars.get('has_product_keywords', False):
            top3_keywords = [kw for kw, _ in product_keywords[:3]]
            auto_insights.append({
                'text': f"상품 키워드 분석 결과, **{', '.join(top3_keywords)}** 등의 키워드가 중요하게 나타났습니다."
            })
        
        if auto_vars.get('has_color_groups', False) and len(color_groups) >= 3:
            auto_insights.append({
                'text': f"색상 그룹 분석 결과, **{color_groups[0][0]}**, **{color_groups[1][0]}**, **{color_groups[2][0]}** 색상군을 중심으로 구성하는 것이 효과적입니다."
            })
        
        auto_vars['auto_insights'] = auto_insights
        
        return auto_vars
    
    # 레거시 메소드 - 마크다운 생성 (하위 호환성 유지)
    def generate_markdown_report(self):
        """
        마크다운 리포트 생성 (레거시 메소드)
        
        Returns:
        - 생성된 리포트 파일 경로
        """
        print("마크다운 리포트 생성은 더 이상 지원되지 않습니다. HTML 리포트를 생성합니다.")
        return self.generate_html_report()