# visualization/insights_formatter.py
from visualization.insights_formatter.summary_generator import SummaryGenerator
from visualization.insights_formatter.insight_text_generator import InsightTextGenerator
from visualization.insights_formatter.execution_guide_generator import ExecutionGuideGenerator
from visualization.insights_formatter.table_data_formatter import TableDataFormatter

class InsightsFormatter:
    """
    통합 Insights Formatter 클래스.
    개별 모듈(요약, 텍스트 생성, 실행 가이드, 테이블 포맷팅)을 통합하여 외부에 단일 인터페이스를 제공합니다.
    """
    def __init__(self, insights):
        self.insights = insights
        self.summary = SummaryGenerator(insights).generate_summary()
        self.text_generator = InsightTextGenerator(self.summary)
        self.guide_generator = ExecutionGuideGenerator(self.summary)
        self.table_formatter = TableDataFormatter(insights)
    
    def generate_insight_text(self, section):
        return self.text_generator.generate_text(section)
    
    def get_execution_guide(self, df=None):
        return self.guide_generator.generate_guide()
    
    def format_table_data(self, data_type):
        return self.table_formatter.format_data(data_type)