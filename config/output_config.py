# config/output_config.py
"""
출력 관련 설정을 제공하는 모듈
"""
from pathlib import Path
from .base_config import BaseConfig

class OutputConfig(BaseConfig):
    """
    출력 폴더, 포트 등 설정 클래스
    """
    
    # 기본 설정값
    DEFAULT_OUTPUT_FOLDER = 'bflow_reports'
    DEFAULT_DASHBOARD_PORT = 8050
    DEFAULT_REPORT_PORT = 8051
    DEFAULT_TEMPLATE_FOLDER = 'templates'
    
    def __init__(self):
        super().__init__()
        
        # 출력 폴더 설정
        self.output_folder = self.get_env_value('BFLOW_OUTPUT_FOLDER', self.DEFAULT_OUTPUT_FOLDER)
        
        # 포트 번호 설정
        self.dashboard_port = self.get_env_int('BFLOW_DASHBOARD_PORT', self.DEFAULT_DASHBOARD_PORT)
        self.report_port = self.get_env_int('BFLOW_REPORT_PORT', self.DEFAULT_REPORT_PORT)
        
        # 템플릿 폴더
        self.template_folder = Path(self.get_env_value('BFLOW_TEMPLATE_FOLDER', self.DEFAULT_TEMPLATE_FOLDER))
    
    def create_output_folders(self):
        """
        필요한 출력 폴더 생성
        
        Returns:
        - 생성된 출력 폴더 경로
        """
        # 기본 출력 폴더
        output_path = Path(self.output_folder)
        output_path.mkdir(exist_ok=True)
        
        # 차트 폴더
        charts_path = output_path / 'charts'
        charts_path.mkdir(exist_ok=True)
        
        return output_path