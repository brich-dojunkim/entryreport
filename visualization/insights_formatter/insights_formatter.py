# visualization/insights_formatter/insights_formatter.py
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
        
        # 요약 정보는 DataProcessor에서 설정하므로 일단 빈 딕셔너리로 초기화
        self.summary = {} 
        
        # summary_generator는 요약 정보가 설정된 후 초기화
        self.summary_generator = None
        self.text_generator = None
        self.guide_generator = None
        
        # 이 모듈은 summary가 필요 없으므로 바로 초기화
        self.table_formatter = TableDataFormatter(insights)
    
    def set_summary(self, summary):
        """
        외부(DataProcessor)에서 요약 정보를 설정합니다.
        """
        self.summary = summary
        
        # 요약 정보가 설정되면 나머지 모듈 초기화
        self.summary_generator = SummaryGenerator(self.summary)
        self.text_generator = InsightTextGenerator(self.summary)
        self.guide_generator = ExecutionGuideGenerator(self.summary)
    
    def generate_insight_text(self, section):
        if self.text_generator is None:
            return ""  # summary가 설정되지 않은 경우
        return self.text_generator.generate_text(section)
    
    def get_execution_guide(self, df=None):
        if self.guide_generator is None:
            return None  # summary가 설정되지 않은 경우
        return self.guide_generator.generate_guide()
    
    def format_table_data(self, data_type):
        return self.table_formatter.format_data(data_type)
        
    def generate_summary_insights(self):
        """
        요약 인사이트 문장들을 생성하여 반환합니다.
        
        Returns:
            list: 요약 인사이트 문장 리스트
        """
        if self.summary_generator is None:
            return []  # summary가 설정되지 않은 경우
        return self.summary_generator.generate_summary_insights()