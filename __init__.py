# __init__.py
"""
비플로우 주문 데이터 분석 시스템 - 대시보드 전용

엑셀 파일에서 주문 데이터를 분석하고, 인사이트 대시보드를 생성합니다.
"""
from data.analyzer import BflowAnalyzer
from data.data_processor.data_processor import DataProcessor
from data.keyword_extractor import KeywordExtractor
from output.dashboard_generator import DashboardGenerator
from config import Config
from visualization.insights_formatter import InsightsFormatter

__version__ = '2.0.0'
__author__ = 'BRICH 김도준'

def create_analysis_workflow(file, output_folder='bflow_reports', config=None):
    """
    파일에서 분석, 대시보드 생성까지의 전체 워크플로우를 생성

    Parameters:
    - file: 엑셀 파일 경로
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
    analyzer.load_data(file)
    insights = analyzer.analyze_data()

    # InsightsFormatter 인스턴스 생성 (재사용을 위해)
    formatter = InsightsFormatter(insights)

    # 대시보드 생성기에 formatter 전달
    dashboard_gen = DashboardGenerator(insights, formatter, output_folder, config)

    return {
        'analyzer': analyzer,
        'data_processor': analyzer.data_processor,
        'insights': insights,
        'formatter': formatter,
        'config': config,
        'dashboard_generator': dashboard_gen
    }

__all__ = [
    'create_analysis_workflow',
    'BflowAnalyzer',
    'DataProcessor',
    'KeywordExtractor',
    'DashboardGenerator',
    'Config'
]