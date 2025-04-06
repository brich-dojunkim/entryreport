# output/data_processor/data_processor.py
"""
통합 데이터 프로세서:
리포트 + 대시보드 양쪽이 필요로 하는 템플릿 변수를 한 번에 구성
(절대 경로로 모듈 임포트)
"""
from datetime import datetime

from output.data_processor.chart_processor import ChartProcessor
from output.data_processor.insight_processor import InsightProcessor
from output.data_processor.recommendation_processor import RecommendationProcessor
from output.data_processor.strategy_processor import StrategyProcessor
from output.data_processor.auto_keyword_processor import AutoKeywordProcessor
from output.data_processor.summary_processor import SummaryProcessor

class DataProcessor:
    """
    '리포트' + '대시보드'가 필요로 하는 모든 키를 하나의 template_vars로 만들어주는 통합 프로세서
    """

    def __init__(self, insights, formatter, now=None, summary=None):
        """
        - insights: 분석 결과 딕셔너리
        - formatter: InsightsFormatter
        - now: datetime 객체 (없으면 현재 시각)
        - summary: 리포트용 요약 정보(없으면 새로 생성)
        """
        self.insights = insights
        self.formatter = formatter
        self.now = now or datetime.now()
        
        # 요약 정보 생성 또는 사용
        if summary is None:
            # SummaryProcessor를 통해 요약 정보 생성
            summary_processor = SummaryProcessor(insights)
            self.summary = summary_processor.generate_summary()
        else:
            self.summary = summary
            
        # formatter에 요약 정보 설정
        if formatter:
            formatter.set_summary(self.summary)

        # 서브 프로세서들 초기화
        self.chart_processor = ChartProcessor(insights, formatter)
        self.insight_processor = InsightProcessor(formatter)
        self.recommendation_processor = RecommendationProcessor(formatter)
        self.strategy_processor = StrategyProcessor(formatter)
        self.auto_keyword_processor = AutoKeywordProcessor()

    def prepare_template_variables(self):
        """
        최종적으로 엑셀 or HTML에서 사용할 template_vars를 생성해서 반환
        """
        template_vars = {}

        # (1) 기본 메타 정보
        template_vars['timestamp'] = self.now.strftime('%Y-%m-%d %H:%M')
        template_vars['period'] = f"{self.insights.get('start_date', '알 수 없음')} ~ {self.insights.get('end_date', '알 수 없음')}"
        template_vars['total_orders'] = len(self.insights.get('df', [])) if 'df' in self.insights else 0
        template_vars['current_year'] = self.now.year

        # 통일된 타이틀/부제
        template_vars['title'] = "엔트리 셀러 통합 인사이트 보고서"
        template_vars['subtitle'] = f"분석 기간: {self.insights.get('start_date')} ~ {self.insights.get('end_date')}"

        # (2) 차트 데이터 (대시보드용)
        chart_data = self.chart_processor.generate_chart_data()  # product_data, color_data, ...
        template_vars.update(chart_data)

        # (3) 대시보드 인사이트 텍스트
        text_insights = self.insight_processor.generate_insights()  # product_insight, color_insight, ...
        template_vars.update(text_insights)

        # (4) 추천 (대시보드/실행가이드)
        recommends = self.recommendation_processor.generate_recommendations()
        template_vars.update(recommends)  # product_recommendations, channel_recommendations, keyword_recommendations

        # (5) 전략 (리포트)
        strat_vars = self.strategy_processor.prepare_strategy_variables(self.insights, self.summary)
        template_vars.update(strat_vars)  # has_strategy, recommended_products, main_price_range ...

        # (6) 자동 키워드 (리포트)
        auto_vars = self.auto_keyword_processor.prepare_auto_keywords_variables(self.insights)
        template_vars.update(auto_vars)  # has_auto_keywords, style_keywords, product_keywords, color_groups, auto_insights

        # (7) 요약 인사이트 (리포트) - InsightsFormatter에 위임
        if self.formatter:
            template_vars['summary_insights'] = self.formatter.generate_summary_insights()
        else:
            template_vars['summary_insights'] = []

        return template_vars