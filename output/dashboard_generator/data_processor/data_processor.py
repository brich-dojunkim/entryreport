# dashboard_generator/data_processor/data_processor.py
"""
대시보드용 데이터 처리 모듈
템플릿 변수 준비 및 데이터 통합 담당
"""
from output.dashboard_generator.data_processor.insight_processor import InsightProcessor
from output.dashboard_generator.data_processor.chart_processor import ChartProcessor
from output.dashboard_generator.data_processor.recommendation_processor import RecommendationProcessor

class DashboardDataProcessor:
    """대시보드 데이터 통합 처리 클래스"""
    
    def __init__(self, insights, formatter):
        """
        데이터 처리기 초기화
        
        Parameters:
        - insights: 분석 결과 딕셔너리
        - formatter: InsightsFormatter 인스턴스
        """
        self.insights = insights
        self.formatter = formatter
        
        # 각 프로세서 초기화
        self.insight_processor = InsightProcessor(formatter)
        self.chart_processor = ChartProcessor(insights, formatter)
        self.recommendation_processor = RecommendationProcessor(formatter)
    
    def prepare_template_variables(self):
        """
        템플릿 변수 준비 및 통합
        
        Returns:
        - 템플릿 변수 딕셔너리
        """
        # 기본 정보
        template_vars = {
            'title': '엔트리 셀러 인사이트 대시보드',
            'subtitle': f'분석 기간: {self.insights.get("start_date", "알 수 없음")} ~ {self.insights.get("end_date", "알 수 없음")}'
        }
        
        # 인사이트 텍스트 데이터 통합
        template_vars.update(self.insight_processor.generate_insights())
        
        # 차트 데이터 통합
        template_vars.update(self.chart_processor.generate_chart_data())
        
        # 추천 데이터 통합
        template_vars.update(self.recommendation_processor.generate_recommendations())
        
        return template_vars