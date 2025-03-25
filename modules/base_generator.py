# modules/base_generator.py
from pathlib import Path
from datetime import datetime
from modules.insights_formatter import InsightsFormatter

class BaseGenerator:
    """
    비플로우 분석 결과를 바탕으로 한 보고서 및 대시보드 생성의 기본 클래스
    """
    
    def __init__(self, insights, output_folder='bflow_reports'):
        """
        생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - output_folder: 결과물 저장 폴더
        """
        self.insights = insights
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # 현재 시간 (파일명용)
        self.now = datetime.now()
        self.timestamp = self.now.strftime("%Y%m%d_%H%M")
        
        # 요약 정보 생성 (공통 모듈 활용)
        self.summary = InsightsFormatter.get_summary(insights)