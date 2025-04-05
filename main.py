# main.py
import os
import argparse
import webbrowser
import threading
import time
from pathlib import Path
from data.analyzer import BflowAnalyzer
from output.report_generator import ReportGenerator
from output.dashboard_generator import DashboardGenerator
from config.config import Config
from visualization.insights_formatter import InsightsFormatter

def create_analysis_workflow(file, output_folder='bflow_reports', config=None, output_format='excel'):
    """
    파일에서 분석, 리포트, 대시보드 생성까지의 전체 워크플로우를 생성
    
    Parameters:
    - file: 엑셀 파일 경로
    - output_folder: 결과물 저장 폴더
    - config: 설정 객체 (None이면 기본 설정 사용)
    - output_format: 출력 형식 ('html' 또는 'excel')
    
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

    report_gen = ReportGenerator(insights, formatter, output_folder, output_format=output_format)
    dashboard_gen = DashboardGenerator(insights, formatter, output_folder, config, output_format=output_format)

    return {
        'analyzer': analyzer,
        'data_processor': analyzer.data_processor,
        'insights': insights,
        'formatter': formatter,
        'config': config,
        'report_generator': report_gen,
        'dashboard_generator': dashboard_gen
    }

def main():
    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(
        description='비플로우 주문 데이터 분석 및 보고서 생성',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # 파일 관련 인수
    parser.add_argument('file', help='엑셀 파일 경로')
    parser.add_argument('--output', '-o', help='결과물 저장 폴더', default='bflow_reports')

    # 출력 관련 인수
    parser.add_argument('--report-only', action='store_true', help='리포트만 생성 (대시보드 생성 안함)')
    parser.add_argument('--dashboard-only', action='store_true', help='대시보드만 생성 (리포트 생성 안함)')
    parser.add_argument('--no-browser', action='store_true', help='브라우저 자동 실행 안함')
    parser.add_argument('--format', choices=['html', 'excel'], default='excel', 
                      help='출력 형식 (기본값: excel)')

    # 대시보드 관련 인수
    parser.add_argument('--port', type=int, help='대시보드 포트 번호 (HTML 모드만 해당)', default=8050)

    args = parser.parse_args()

    try:
        # 워크플로우 실행
        workflow = create_analysis_workflow(
            args.file,
            args.output,
            output_format=args.format
        )

        # 리포트 생성 (report_only 또는 기본 모드)
        if not args.dashboard_only:
            print("리포트 생성 중...")
            report_path = workflow['report_generator'].generate_html_report()  # 메소드명은 유지하되 내부에서 엑셀 생성

            if report_path and os.path.exists(report_path) and not args.no_browser:
                print(f"리포트가 생성되었습니다: {report_path}")
                # HTML일 경우 브라우저에서 열기 (엑셀은 내부에서 처리)
                if args.format.lower() == 'html':
                    webbrowser.open(f"file://{Path(report_path).resolve()}")

        # 대시보드 생성 (dashboard_only 또는 기본 모드)
        if not args.report_only:
            print("대시보드 생성 중...")
            dashboard_gen = workflow['dashboard_generator']

            # HTML 모드일 경우 별도 스레드로 실행 (기존 방식)
            if args.format.lower() == 'html':
                dashboard_thread = threading.Thread(
                    target=dashboard_gen.generate_dashboard,
                    args=(args.port, not args.no_browser)
                )
                dashboard_thread.daemon = True
                dashboard_thread.start()

                print(f"대시보드 서버가 시작되었습니다: http://127.0.0.1:{args.port}")
                print("대시보드를 종료하려면 Ctrl+C를 누르세요.")

                try:
                    while dashboard_thread.is_alive():
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n대시보드 서버가 종료되었습니다.")
                    return 0
            else:
                # 엑셀 모드일 경우 즉시 실행
                dashboard_path = dashboard_gen.generate_dashboard(None, not args.no_browser)
                if dashboard_path:
                    print(f"대시보드가 생성되었습니다: {dashboard_path}")

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