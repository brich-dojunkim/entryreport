# output/report_generator/report_generator.py
"""
비플로우 분석 결과를 바탕으로 HTML 리포트를 생성하는 메인 클래스 (간소화 버전)
"""
from pathlib import Path
from flask import Flask, render_template
from datetime import datetime
from output.base_generator import BaseGenerator

from output.report_generator.data_processor.data_processor import ReportDataProcessor
from output.report_generator.template_handler import TemplateHandler

class ReportGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 HTML 리포트 생성 (간소화 버전)"""

    def __init__(self, insights, formatter=None, output_folder='bflow_reports'):
        """
        리포트 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - formatter: InsightsFormatter 인스턴스 (None이면 자동 생성)
        - output_folder: 결과물 저장 폴더
        """
        super().__init__(insights, formatter, output_folder)
        self.chart_folder = self.output_folder / 'charts'
        self.chart_folder.mkdir(exist_ok=True)
        self.template_folder = Path('templates')

        self.data_processor = ReportDataProcessor(insights, formatter)
        self.template_handler = TemplateHandler(self.template_folder)

    def generate_html_report(self):
        """
        HTML 리포트 생성 (간소화 버전)
        """
        print("간소화된 HTML 리포트를 생성합니다...")
        html_file = self.output_folder / f"bflow_report_{self.timestamp}.html"

        try:
            # 템플릿 변수 준비
            template_vars = self.data_processor.prepare_template_variables(
                now=self.now,
                summary=self.summary
            )

            # 템플릿 렌더링 (간소화 템플릿)
            output_html = self.template_handler.render_template(
                'report_template.html',
                **template_vars
            )

            # HTML 파일 저장
            saved_path = self.template_handler.save_html(output_html, html_file)
            if saved_path:
                print(f"HTML 리포트가 생성되었습니다: {saved_path}")
                return saved_path
            else:
                print("리포트 파일 저장 실패")
                return None

        except Exception as e:
            print(f"HTML 리포트 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_web_report(self, port=8051, open_browser=True):
        """
        웹 서버로 인터랙티브 HTML 리포트 표시 (간소화 버전)
        """
        print(f"웹 리포트 서버 시작 중... (포트: {port})")

        template_vars = self.data_processor.prepare_template_variables(
            now=self.now,
            summary=self.summary
        )

        app = Flask(__name__,
                    template_folder=str(self.template_folder),
                    static_folder=str(self.chart_folder))

        @app.route('/')
        def index():
            return render_template('report_template.html', **template_vars)

        try:
            app.run(host='127.0.0.1', port=port, debug=False)
        except Exception as e:
            print(f"웹 리포트 서버 실행 중 오류 발생: {e}")

        return f'http://127.0.0.1:{port}'

    def generate_markdown_report(self):
        """
        레거시 메소드 - 마크다운 리포트 생성
        """
        print("마크다운 리포트 생성 대신 HTML 리포트를 생성합니다. (간소화 버전)")
        return self.generate_html_report()
