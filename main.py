# main.py
import os
import argparse
import webbrowser
import threading
import time
from pathlib import Path
from data.analyzer.analyzer import BflowAnalyzer
from output.dashboard_generator import DashboardGenerator
from config import Config
from visualization.insights_formatter import InsightsFormatter

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
    if config is None:
        config = Config()
        config.output_folder = output_folder

    analyzer = BflowAnalyzer(config)
    analyzer.load_data(file)
    insights = analyzer.analyze_data()

    formatter = InsightsFormatter(insights)
    dashboard_gen = DashboardGenerator(insights, formatter, output_folder, config)

    return {
        'analyzer': analyzer,
        'data_processor': analyzer.data_processor,
        'insights': insights,
        'formatter': formatter,
        'config': config,
        'dashboard_generator': dashboard_gen
    }

def main():
    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(
        description='비플로우 주문 데이터 분석 및 대시보드 생성',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # 파일 관련 인수
    parser.add_argument('file', help='엑셀 파일 경로')
    parser.add_argument('--output', '-o', help='결과물 저장 폴더', default='bflow_reports')

    # 출력 관련 인수
    parser.add_argument('--no-browser', action='store_true', help='브라우저 자동 실행 안함')
    parser.add_argument('--no-pdf', action='store_true', help='PDF 생성 안함')
    parser.add_argument('--pdf-only', action='store_true', help='PDF만 생성 (브라우저 실행 안함)')

    # 대시보드 관련 인수
    parser.add_argument('--port', type=int, help='대시보드 포트 번호', default=8050)
    
    # Playwright 설치 옵션
    parser.add_argument('--install-browsers', action='store_true', help='Playwright 브라우저 설치')

    args = parser.parse_args()

    try:
        # Playwright 브라우저 설치 옵션
        if args.install_browsers:
            print("Playwright 브라우저 설치 중...")
            workflow = create_analysis_workflow(args.file, args.output)
            dashboard_gen = workflow['dashboard_generator']
            if dashboard_gen.install_playwright_browsers():
                print("Playwright 브라우저 설치가 완료되었습니다.")
                return 0
            else:
                print("Playwright 브라우저 설치에 실패했습니다.")
                return 1

        # 워크플로우 실행
        workflow = create_analysis_workflow(
            args.file,
            args.output
        )

        # 대시보드 생성 옵션 설정
        open_browser = not args.no_browser and not args.pdf_only
        save_pdf = not args.no_pdf

        print("대시보드 생성 중...")
        dashboard_gen = workflow['dashboard_generator']

        # 대시보드 생성
        result = dashboard_gen.generate_dashboard(
            port=args.port,
            open_browser=open_browser,
            save_pdf=save_pdf
        )

        if result:
            print("\n" + "="*50)
            print("대시보드 생성 완료!")
            print("="*50)
            
            if 'html' in result:
                print(f"📄 HTML 파일: {result['html']}")
            
            if 'pdf' in result:
                print(f"📋 PDF 파일:  {result['pdf']}")
                print("   ✅ 웹페이지 전체가 하나의 긴 PDF로 저장됨")
                print("   ✅ A4 용지로 나뉘지 않고 연속된 문서")
            
            print("="*50)
            
            # PDF만 생성하는 경우 브라우저를 열지 않고 종료
            if args.pdf_only:
                print("PDF 생성이 완료되었습니다.")
                return 0
            
            # 브라우저가 열린 경우 사용자 입력 대기
            if open_browser:
                print("\n브라우저에서 대시보드를 확인하세요.")
                print("종료하려면 Enter를 누르세요...")
                input()
        else:
            print("대시보드 생성에 실패했습니다.")
            return 1

        print("처리 완료")
        return 0

    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1

# 스크립트 실행
if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n사용자에 의해 중단되었습니다.")
        exit(0)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)