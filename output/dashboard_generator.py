# output/dashboard_generator.py
"""
비플로우 분석 결과를 바탕으로 HTML 대시보드 및 PDF 생성하는 메인 클래스
"""
import webbrowser
import asyncio
import os
from pathlib import Path
from output.base_generator import BaseGenerator
from config import Config
from utils import convert_to_serializable
from output.data_processor.data_processor import DataProcessor
from output.formatters.template_handler import TemplateHandler


class DashboardGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 HTML 대시보드 및 PDF 생성"""
    
    def __init__(self, insights, formatter=None, output_folder='bflow_reports', config=None):
        """
        대시보드 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - formatter: InsightsFormatter 인스턴스 (None이면 자동 생성)
        - output_folder: 결과물 저장 폴더
        - config: 설정 객체 (None이면 기본 설정 사용)
        """
        super().__init__(insights, formatter, output_folder)
        
        # 설정 객체 설정
        if config is None:
            self.config = Config()
        else:
            self.config = config
        
        # 템플릿 경로 설정
        self.template_folder = Path(self.config.template_folder)
        
        # 데이터 처리기
        self.data_processor = DataProcessor(insights, self.formatter)

        # 템플릿 핸들러
        self.template_handler = TemplateHandler(self.template_folder)
    
    def generate_dashboard(self, port=None, open_browser=True, save_pdf=True):
        """
        HTML 대시보드 생성 및 실행
        
        Parameters:
        - port: 대시보드 실행 포트 (None이면 설정에서 가져옴)
        - open_browser: 브라우저 자동 실행 여부
        - save_pdf: PDF 파일 생성 여부
        
        Returns:
        - 생성된 대시보드 파일 경로들의 딕셔너리 {'html': path, 'pdf': path}
        """
        print("HTML 대시보드 생성 중...")
        
        try:
            # 포트 설정 (필요한 경우)
            if port is None:
                port = self.config.dashboard_port
                
            # 템플릿 변수 준비
            template_vars = self.data_processor.prepare_template_variables()
            
            # Guide 객체 가져오기
            if self.formatter:
                guide = self.formatter.get_execution_guide()
            else:
                guide = None
            
            # 속성 키워드 데이터 처리
            if guide:
                # 색상 키워드 - 더 많은 색상 제공
                if 'color_keywords' in guide and guide['color_keywords']:
                    template_vars['color_keywords'] = guide['color_keywords']
                
                # 소재 키워드 - 더 많은 소재 제공
                if 'material_keywords' in guide and guide['material_keywords']:
                    template_vars['material_keywords'] = guide['material_keywords']
                
                # 디자인 키워드 - 더 많은 디자인 제공
                if 'design_keywords' in guide and guide['design_keywords']:
                    template_vars['design_keywords'] = guide['design_keywords']
                
                # 스타일 키워드 (핏 & 실루엣) - 추가
                if 'fit_style_keywords' in guide and guide['fit_style_keywords']:
                    template_vars['style_keywords'] = guide['fit_style_keywords']
                elif 'auto_style_keywords' in guide and guide['auto_style_keywords']:
                    # 자동 추출 스타일 키워드에서 가져오기
                    auto_style = []
                    for item in guide['auto_style_keywords']:
                        if isinstance(item, str):
                            auto_style.append(item)
                        elif isinstance(item, dict) and 'name' in item:
                            auto_style.append(item['name'])
                    template_vars['style_keywords'] = auto_style
            
            # 직렬화 가능한 형식으로 변환 (차트 데이터만)
            for key in template_vars:
                if key in ['product_data', 'color_data', 'price_data', 'channel_data', 
                        'size_data', 'material_data', 'design_data', 'bestseller_data']:
                    template_vars[key] = convert_to_serializable(template_vars[key])
            
            # 템플릿 렌더링
            output = self.template_handler.render_template('dashboard_template.html', **template_vars)
            
            # HTML 파일 저장
            dashboard_file = self.output_folder / f"dashboard_{self.timestamp}.html"
            html_path = self.template_handler.save_html(output, dashboard_file)
            
            result = {}
            
            if html_path:
                print(f"HTML 대시보드가 생성되었습니다: {html_path}")
                result['html'] = str(html_path)
                
                # PDF 생성
                if save_pdf:
                    pdf_path = self.generate_pdf_from_html(html_path)
                    if pdf_path:
                        result['pdf'] = str(pdf_path)
                        print(f"PDF 대시보드가 생성되었습니다: {pdf_path}")
                        print("✅ 웹페이지 전체가 하나의 연속된 PDF로 저장되었습니다")
                
                # 브라우저에서 열기
                if open_browser:
                    webbrowser.open(f"file://{html_path.resolve()}")
                
                return result
            else:
                print("대시보드 파일 저장 실패")
                return None
                
        except Exception as e:
            print(f"HTML 대시보드 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_pdf_from_html(self, html_path):
        """
        HTML 파일을 PDF로 변환
        
        Parameters:
        - html_path: HTML 파일 경로
        
        Returns:
        - 생성된 PDF 파일 경로
        """
        try:
            # PDF 파일 경로 생성
            pdf_path = html_path.with_suffix('.pdf')
            
            # Playwright를 사용한 PDF 생성 시도
            pdf_result = self._generate_pdf_with_playwright(html_path, pdf_path)
            
            if pdf_result:
                return pdf_result
            
            # Playwright 실패 시 WeasyPrint로 대체
            print("Playwright PDF 생성 실패, WeasyPrint로 시도...")
            return self._generate_pdf_with_weasyprint(html_path, pdf_path)
            
        except Exception as e:
            print(f"PDF 생성 중 오류 발생: {e}")
            return None

    def _generate_pdf_with_playwright(self, html_path, pdf_path):
        """
        Playwright를 사용하여 웹페이지 전체를 하나의 PDF로 생성
        """
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                # 브라우저 시작 (더 큰 뷰포트 설정)
                browser = p.chromium.launch()
                page = browser.new_page(viewport={'width': 1200, 'height': 800})
                
                # HTML 파일 로드
                page.goto(f"file://{html_path.resolve()}")
                
                # 페이지가 완전히 로드될 때까지 대기
                page.wait_for_load_state('networkidle')
                
                # 차트가 렌더링될 시간을 줌
                page.wait_for_timeout(3000)
                
                # 페이지의 실제 크기 측정
                content_size = page.evaluate("""
                    () => {
                        const body = document.body;
                        const html = document.documentElement;
                        const height = Math.max(
                            body.scrollHeight,
                            body.offsetHeight,
                            html.clientHeight,
                            html.scrollHeight,
                            html.offsetHeight
                        );
                        const width = Math.max(
                            body.scrollWidth,
                            body.offsetWidth,
                            html.clientWidth,
                            html.scrollWidth,
                            html.offsetWidth
                        );
                        return { width, height };
                    }
                """)
                
                print(f"페이지 크기: {content_size['width']}x{content_size['height']}px")
                
                # 웹페이지 전체를 하나의 PDF로 생성 (용지 크기를 콘텐츠에 맞춤)
                page.pdf(
                    path=str(pdf_path),
                    width=f"{content_size['width']}px",
                    height=f"{content_size['height']}px",
                    print_background=True,
                    margin={
                        'top': '0px',
                        'bottom': '0px', 
                        'left': '0px',
                        'right': '0px'
                    },
                    prefer_css_page_size=False  # CSS 페이지 크기 무시
                )
                
                browser.close()
                return pdf_path
                
        except ImportError:
            print("Playwright가 설치되지 않았습니다. pip install playwright && playwright install 실행하세요.")
            return None
        except Exception as e:
            print(f"Playwright PDF 생성 오류: {e}")
            return None

    def _generate_pdf_with_weasyprint(self, html_path, pdf_path):
        """
        WeasyPrint를 사용하여 웹페이지 전체를 하나의 PDF로 생성 (백업 방법)
        """
        try:
            import weasyprint
            from weasyprint import CSS, HTML
            
            # HTML 파일 읽기
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 페이지 분할을 방지하는 CSS 추가
            additional_css = CSS(string="""
                @page {
                    size: auto;
                    margin: 0;
                }
                
                body {
                    margin: 0;
                    padding: 20px;
                }
                
                * {
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                }
                
                .chart-container,
                .keywords-container,
                .dashboard-header {
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                }
                
                .row {
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                }
            """)
            
            # HTML을 PDF로 변환
            html_doc = HTML(string=html_content, base_url=str(html_path.parent))
            html_doc.write_pdf(str(pdf_path), stylesheets=[additional_css])
            
            return pdf_path
            
        except ImportError:
            print("WeasyPrint가 설치되지 않았습니다. pip install weasyprint 실행하세요.")
            return None
        except Exception as e:
            print(f"WeasyPrint PDF 생성 오류: {e}")
            return None

    def install_playwright_browsers(self):
        """
        Playwright 브라우저 설치 (최초 설정용)
        """
        try:
            import subprocess
            result = subprocess.run(['playwright', 'install'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Playwright 브라우저 설치 완료")
                return True
            else:
                print(f"Playwright 브라우저 설치 실패: {result.stderr}")
                return False
        except Exception as e:
            print(f"Playwright 브라우저 설치 중 오류: {e}")
            return False