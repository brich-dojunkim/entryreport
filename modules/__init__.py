# modules/__init__.py
from .analyzer import BflowAnalyzer
from .data_processor import DataProcessor
from .chart_generator import ChartGenerator
from .report_generator import ReportGenerator
from .dashboard_generator import DashboardGenerator
from .insights_formatter import InsightsFormatter
from .base_generator import BaseGenerator
from .keyword_extractor import KeywordExtractor
from .config import Config

# 버전 정보 등 패키지 메타데이터
__version__ = '1.2.0'  # 구조 개선 및 설정 클래스 도입 버전
__author__ = 'BRICH 개발팀'

# 패키지 전체의 공통 기능 함수 정의
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