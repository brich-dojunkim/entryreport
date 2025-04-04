# dashboard_generator/dashboard_generator.py
"""
비플로우 분석 결과를 바탕으로 대시보드 생성하는 메인 클래스
"""
import webbrowser
from pathlib import Path
from output.base_generator import BaseGenerator
from config.config import Config
from utils.utils import convert_to_serializable
from output.dashboard_generator.data_processor.data_processor import DashboardDataProcessor
from output.dashboard_generator.template_handler import TemplateHandler

class DashboardGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 대시보드 생성"""
    
    def __init__(self, insights, formatter=None, output_folder='bflow_reports', config=None):
        """
        대시보드 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - formatter: InsightsFormatter 인스턴스 (None이면 자동 생성)
        - output_folder: 결과물 저장 폴더
        - config: 설정 객체 (None이면 기본 설정 사용)
        """
        # 부모 클래스 초기화
        super().__init__(insights, formatter, output_folder)
        
        # 설정 객체 설정
        if config is None:
            self.config = Config()
        else:
            self.config = config
        
        # 템플릿 경로 설정
        self.template_folder = Path(self.config.template_folder)
        
        # 데이터 처리기 및 템플릿 핸들러 생성
        self.data_processor = DashboardDataProcessor(insights, self.formatter)
        self.template_handler = TemplateHandler(self.template_folder)
        
        # 디버깅 정보 출력
        print(f"DashboardGenerator 초기화 - insights 타입: {type(insights)}")
        print(f"DashboardGenerator 초기화 - summary 타입: {type(self.summary)}")
    
    def generate_dashboard(self, port=None, open_browser=True):
        """
        대시보드 생성 및 실행
        
        Parameters:
        - port: 대시보드 실행 포트 (None이면 설정에서 가져옴)
        - open_browser: 브라우저 자동 실행 여부
        
        Returns:
        - 생성된 대시보드 URL
        """
        print("대시보드 생성 중...")
        
        try:
            # 포트 설정 (필요한 경우)
            if port is None:
                port = self.config.dashboard_port
                
            # 템플릿 변수 준비
            template_vars = self.data_processor.prepare_template_variables()
            
            # 모든 데이터를 직렬화 가능한 형식으로 변환
            for key in template_vars:
                if key in ['product_data', 'color_data', 'price_data', 'channel_data', 
                        'size_data', 'material_design_data', 'bestseller_data']:
                    template_vars[key] = convert_to_serializable(template_vars[key])
            
            # 템플릿 렌더링
            output = self.template_handler.render_template('dashboard_template.html', **template_vars)
            
            # HTML 파일 저장
            dashboard_file = self.output_folder / f"dashboard_{self.timestamp}.html"
            saved_path = self.template_handler.save_html(output, dashboard_file)
            
            if saved_path:
                print(f"HTML 대시보드가 생성되었습니다: {saved_path}")
                
                # 브라우저에서 열기
                if open_browser:
                    webbrowser.open(f"file://{saved_path.resolve()}")
                
                return str(saved_path)
            else:
                print("대시보드 파일 저장 실패")
                return None
                
        except Exception as e:
            print(f"대시보드 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None