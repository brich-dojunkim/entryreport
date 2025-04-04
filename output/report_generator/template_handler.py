# output/report_generator/template_handler.py
"""
리포트 템플릿 처리 모듈
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateHandler:
    """리포트 템플릿 처리 클래스"""
    
    def __init__(self, template_folder):
        """
        템플릿 처리기 초기화
        """
        self.template_folder = Path(template_folder)
        self.env = Environment(loader=FileSystemLoader(self.template_folder))
    
    def render_template(self, template_name, **context):
        """
        템플릿 렌더링
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def save_html(self, html_content, output_path):
        """
        HTML 파일 저장
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        except Exception as e:
            print(f"HTML 파일 저장 중 오류 발생: {e}")
            return None
