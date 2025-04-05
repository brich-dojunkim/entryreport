# 파일 위치 예시: output/data_processor.py
"""
통합 데이터 처리 모듈: 리포트 + 대시보드 템플릿 변수를 한 번에 준비
"""
from datetime import datetime

# 아래 임포트들은 기존 코드의 경로에 맞춰 조정하세요.
# report 쪽:
from output.report_generator.data_processor.strategy_processor import StrategyProcessor
from output.report_generator.data_processor.auto_keyword_processor import AutoKeywordProcessor

# dashboard 쪽:
from output.dashboard_generator.data_processor.insight_processor import InsightProcessor
from output.dashboard_generator.data_processor.chart_processor import ChartProcessor
from output.dashboard_generator.data_processor.recommendation_processor import RecommendationProcessor


class DataProcessor:
    """
    리포트와 대시보드 양쪽의 템플릿 변수를 한 번에 생성하는 통합 프로세서.
    """

    def __init__(self, insights, formatter, now=None, summary=None):
        """
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과 (dict)
        - formatter: InsightsFormatter 인스턴스
        - now: datetime (기본값 None이면 현재 시각)
        - summary: 리포트에 쓰이는 요약 정보 (dict, 기본값 None이면 {})
        """
        self.insights = insights
        self.formatter = formatter

        self.now = now or datetime.now()
        self.summary = summary or {}

        # [리포트] 관련 서브 프로세서
        self.strategy_processor = StrategyProcessor(formatter)
        self.auto_keyword_processor = AutoKeywordProcessor()
        
        # [대시보드] 관련 서브 프로세서
        self.insight_processor = InsightProcessor(formatter)
        self.chart_processor = ChartProcessor(insights, formatter)
        self.recommendation_processor = RecommendationProcessor(formatter)

    def prepare_template_variables(self):
        """
        통합된 템플릿 변수를 생성하여 반환합니다.
        
        Returns:
        - template_vars (dict): 리포트 + 대시보드 모두를 커버하는 키가 들어있음.
        """
        # 1) 공통/기본 정보
        template_vars = {
            'title': '엔트리 셀러 통합 인사이트 보고서',
            'timestamp': self.now.strftime('%Y-%m-%d %H:%M'),
            'period': f"{self.insights.get('start_date', '알 수 없음')} ~ {self.insights.get('end_date', '알 수 없음')}",
            'total_orders': len(self.insights.get('df', [])) if 'df' in self.insights else self.summary.get('total_orders', 0),
            'current_year': self.now.year,
        }

        # (2) 리포트용 요약 정보 (summary_insights 등)
        #     _prepare_summary_variables는 report_data_processor의 _prepare_summary_variables 로직을 통합/이식
        template_vars.update(self._prepare_summary_variables(self.summary))

        # (3) 자동 키워드 (report_generator.data_processor.auto_keyword_processor)
        #     예: has_auto_keywords, has_style_keywords, style_keywords, product_keywords, color_groups, auto_insights 등
        template_vars.update(self.auto_keyword_processor.prepare_auto_keywords_variables(self.insights))

        # (4) 전략 정보 (report_generator.data_processor.strategy_processor)
        #     예: has_strategy, recommended_products, main_price_range, main_price_percent, has_channels, top_channels, keyword_recommendations
        template_vars.update(self.strategy_processor.prepare_strategy_variables(self.insights, self.summary))

        # (5) 대시보드용 인사이트 텍스트
        #     예: product_insight, color_insight, price_insight, channel_insight, size_insight, ...
        template_vars.update(self.insight_processor.generate_insights())

        # (6) 대시보드용 차트 데이터
        #     예: product_data, color_data, price_data, channel_data, size_data, material_design_data, ...
        template_vars.update(self.chart_processor.generate_chart_data())

        # (7) 대시보드용 추천 (recommendation_processor)
        #     예: product_recommendations, channel_recommendations, keyword_recommendations
        template_vars.update(self.recommendation_processor.generate_recommendations())

        # 필요하다면 'subtitle' 등 추가:
        template_vars['subtitle'] = f"분석 기간: {self.insights.get('start_date', '')} ~ {self.insights.get('end_date', '')}"

        # 통합된 템플릿 변수 반환
        return template_vars

    def _prepare_summary_variables(self, summary):
        """
        예시: report_data_processor.ReportDataProcessor._prepare_summary_variables 의 로직을 그대로 가져온 예
        """
        summary_points = []

        # 상품군 인사이트
        if 'top_keywords' in summary and summary['top_keywords']:
            first_kw = summary['top_keywords'][0]
            summary_points.append(
                f"가장 많이 팔린 상품 유형은 '{first_kw['name']}'이며 총 {first_kw['count']}건 판매되었습니다."
            )
        else:
            summary_points.append("상품군 데이터를 확인할 수 없습니다.")

        # 채널 인사이트
        if 'top3_channels' in summary and summary['top3_channels']:
            ch = summary['top3_channels'][0]
            summary_points.append(f"주요 판매 채널은 '{ch}'가 가장 큰 비중을 차지합니다.")
        else:
            summary_points.append("판매 채널 데이터가 부족합니다.")

        # 가격대 인사이트
        if 'main_price_range' in summary and 'main_price_percent' in summary:
            summary_points.append(
                f"{summary['main_price_range']} 가격대가 전체 중 {summary['main_price_percent']:.1f}%로 가장 많이 판매되었습니다."
            )
        else:
            summary_points.append("가격대 분석 데이터가 충분하지 않습니다.")

        # 색상 인사이트 (예시)
        if 'top_colors' in summary and summary['top_colors']:
            summary_points.append(f"가장 인기 있는 색상은 '{summary['top_colors'][0]['name']}'입니다.")

        return {
            'summary_insights': summary_points
        }
