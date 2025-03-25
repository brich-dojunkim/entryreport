from .analyzer import BflowAnalyzer
from .chart_generator import ChartGenerator
from .report_generator import ReportGenerator
from .dashboard_generator import DashboardGenerator
from .insights_formatter import InsightsFormatter
from .base_generator import BaseGenerator
from .keyword_extractor import KeywordExtractor

# 버전 정보 등 패키지 메타데이터
__version__ = '1.1.0'  # 자동 키워드 추출 및 HTML 리포트 지원 버전
__author__ = 'BRICH 개발팀'

# 패키지 전체의 공통 기능 함수 정의
def create_analysis_workflow(file1, file2=None, output_folder='bflow_reports'):
    """
    파일에서 분석, 리포트, 대시보드 생성까지의 전체 워크플로우를 생성
    
    Parameters:
    - file1: 첫 번째 엑셀 파일 경로
    - file2: 두 번째 엑셀 파일 경로 (선택사항)
    - output_folder: 결과물 저장 폴더
    
    Returns:
    - 분석 워크플로우 구성요소 딕셔너리
    """
    analyzer = BflowAnalyzer()
    analyzer.load_data(file1, file2)
    insights = analyzer.analyze_data()
    
    report_gen = ReportGenerator(insights, output_folder)
    dashboard_gen = DashboardGenerator(insights, output_folder)
    
    return {
        'analyzer': analyzer,
        'insights': insights,
        'report_generator': report_gen,
        'dashboard_generator': dashboard_gen
    }