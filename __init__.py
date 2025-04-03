"""
비플로우 주문 데이터 분석 시스템

엑셀 파일에서 주문 데이터를 분석하고, 인사이트 리포트와 대시보드를 생성합니다.
"""
from data.analyzer import BflowAnalyzer
from data.data_processor import DataProcessor
from output.report_generator import ReportGenerator
from output.dashboard_generator import DashboardGenerator
from config.config import Config
from visualization.insights_formatter import InsightsFormatter

__version__ = '1.2.0'
__author__ = 'BRICH 개발팀'

def create_analysis_workflow(file1, file2=None, output_folder='bflow_reports', config=None):
    """
    파일에서 분석, 리포트, 대시보드 생성까지의 전체 워크플로우를 생성

    Parameters:
    - file1: 첫 번째 엑셀 파일 경로
    - file2: 두 번째 엑셀 파일 경로 (선택사항)
    - output_folder: 결과물 저장 폴더
    - config: 설정 객체 (None이면 기본 설정 사용)

    Returns:
    - 분석 워크플로우 구성요소 딕셔너리
    """
    # 설정 객체 생성
    if config is None:
        config = Config()
        config.output_folder = output_folder

    # 분석기 생성 및 데이터 로드
    analyzer = BflowAnalyzer(config)
    analyzer.load_data(file1, file2)
    insights = analyzer.analyze_data()

    # InsightsFormatter 인스턴스 생성 (재사용을 위해)
    formatter = InsightsFormatter(insights)

    # 생성기 클래스들에 formatter 전달
    report_gen = ReportGenerator(insights, formatter, output_folder)
    dashboard_gen = DashboardGenerator(insights, formatter, output_folder)

    return {
        'analyzer': analyzer,
        'data_processor': analyzer.data_processor,
        'insights': insights,
        'formatter': formatter,
        'config': config,
        'report_generator': report_gen,
        'dashboard_generator': dashboard_gen
    }

__all__ = [
    'create_analysis_workflow',
    'BflowAnalyzer',
    'DataProcessor',
    'ReportGenerator',
    'DashboardGenerator',
    'Config'
]
