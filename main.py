import os
import argparse
import webbrowser
import threading
import time
from pathlib import Path

# 개선된 import 방식
from modules import create_analysis_workflow

def main():
    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(
        description='비플로우 주문 데이터 분석 및 보고서 생성',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # 파일 관련 인수
    parser.add_argument('file1', help='첫 번째 엑셀 파일 경로')
    parser.add_argument('--file2', help='두 번째 엑셀 파일 경로 (선택사항)', default=None)
    parser.add_argument('--output', '-o', help='결과물 저장 폴더', default='bflow_reports')
    
    # 출력 관련 인수
    parser.add_argument('--report-only', action='store_true', help='리포트만 생성 (대시보드 생성 안함)')
    parser.add_argument('--dashboard-only', action='store_true', help='대시보드만 생성 (리포트 생성 안함)')
    parser.add_argument('--no-browser', action='store_true', help='브라우저 자동 실행 안함')
    
    # 대시보드 관련 인수
    parser.add_argument('--port', type=int, help='대시보드 포트 번호', default=8050)
    
    args = parser.parse_args()
    
    try:
        # 개선된 워크플로우 함수 사용
        workflow = create_analysis_workflow(
            args.file1,
            args.file2,
            args.output
        )
        
        # 리포트 생성 (report_only 또는 기본 모드)
        if not args.dashboard_only:
            print("리포트 생성 중...")
            
            # HTML 리포트 생성
            report_path = workflow['report_generator'].generate_html_report()
            
            # 리포트 파일 열기
            if report_path and os.path.exists(report_path) and not args.no_browser:
                print(f"리포트가 생성되었습니다: {report_path}")
                webbrowser.open(f"file://{report_path.resolve()}")
        
        # 대시보드 생성 (dashboard_only 또는 기본 모드)
        if not args.report_only:
            print("대시보드 생성 중...")
            dashboard_gen = workflow['dashboard_generator']
            
            # 대시보드 스레드 시작
            dashboard_thread = threading.Thread(
                target=dashboard_gen.generate_dashboard,
                args=(args.port, not args.no_browser)
            )
            dashboard_thread.daemon = True
            dashboard_thread.start()
            
            print(f"대시보드 서버가 시작되었습니다: http://127.0.0.1:{args.port}")
            print("대시보드를 종료하려면 Ctrl+C를 누르세요.")
            
            # 대시보드 서버가 종료될 때까지 기다림
            try:
                while dashboard_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n대시보드 서버가 종료되었습니다.")
                return 0
        
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