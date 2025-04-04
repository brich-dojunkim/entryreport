# dashboard_generator/template_handler.py
"""
대시보드 템플릿 처리 모듈
템플릿 렌더링 및 파일 저장 담당
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateHandler:
    """대시보드 템플릿 처리 클래스"""
    
    def __init__(self, template_folder):
        """
        템플릿 처리기 초기화
        
        Parameters:
        - template_folder: 템플릿 파일이 있는 폴더 경로
        """
        self.template_folder = Path(template_folder)
        self.env = Environment(loader=FileSystemLoader(self.template_folder))
    
    def render_template(self, template_name, **context):
        """
        템플릿 렌더링
        
        Parameters:
        - template_name: 템플릿 파일명
        - context: 템플릿 컨텍스트 (변수)
        
        Returns:
        - 렌더링된 HTML 문자열
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def save_html(self, html_content, output_path):
        """
        HTML 파일 저장
        
        Parameters:
        - html_content: 저장할 HTML 내용
        - output_path: 저장할 파일 경로
        
        Returns:
        - 저장된 파일 경로
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        except Exception as e:
            print(f"HTML 파일 저장 중 오류 발생: {e}")
            return None