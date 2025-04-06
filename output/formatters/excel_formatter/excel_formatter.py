# output/formatters/excel_formatter/excel_formatter.py
"""
비플로우 분석 결과를 엑셀 포맷으로 변환하는 메인 클래스 (ExcelFormatter).
HTML과 유사한 레이아웃으로 엑셀 시트 생성
"""
import pandas as pd
from pathlib import Path

# 시트별 생성 로직을 import
from .sheets.report_sheet import create_report_sheet
from .sheets.dashboard_sheet import create_dashboard_sheet


class ExcelFormatter:
    """
    인사이트 데이터를 엑셀 파일로 포맷팅하는 클래스
    """

    def __init__(self, insights_formatter=None):
        """
        엑셀 포맷터 초기화

        Parameters:
        - insights_formatter: InsightsFormatter 인스턴스 (데이터 변환에 사용)
        """
        self.formatter = insights_formatter

    def generate_excel(self, template_vars, output_path):
        """
        템플릿 변수를 바탕으로 엑셀 파일 생성

        Parameters:
        - template_vars: 템플릿 변수 딕셔너리 (기존 HTML 템플릿에 사용되던 변수들)
        - output_path: 출력 파일 경로

        Returns:
        - 생성된 파일 경로
        """
        try:
            # 엑셀 작성기 생성 (XlsxWriter 엔진 사용)
            writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

            # 리포트 시트 생성
            create_report_sheet(writer, template_vars)

            # 대시보드 시트 생성
            create_dashboard_sheet(writer, template_vars)

            # 작성기 저장 및 닫기
            writer.close()

            return output_path

        except Exception as e:
            print(f"엑셀 파일 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None
