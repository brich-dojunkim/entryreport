# output/formatters/template_handler.py
"""
HTML 템플릿 핸들러 - Jinja2를 사용한 HTML 생성
"""
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader

class TemplateHandler:
    """
    HTML 템플릿 처리 클래스
    """
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
        HTML 템플릿 렌더링
        
        Parameters:
        - template_name: 템플릿 파일명
        - context: 템플릿 컨텍스트 (변수)
        
        Returns:
        - 렌더링된 HTML 문자열
        """
        # 디버깅: keyword_recommendations 데이터 구조 출력
        if 'keyword_recommendations' in context:
            print(f"[디버깅-Template] keyword_recommendations 개수: {len(context['keyword_recommendations'])}")
            for i, item in enumerate(context['keyword_recommendations']):
                # 각 항목의 구조 확인
                print(f"[디버깅-Template] 키워드 {i+1} 구조: {json.dumps(item, default=str)}")
                if 'category' in item:
                    print(f"[디버깅-Template] 키워드 {i+1} 카테고리: {item['category']}")
                else:
                    print(f"[디버깅-Template] 키워드 {i+1}에 카테고리 속성 없음")
        
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