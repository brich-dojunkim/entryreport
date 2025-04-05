# output/formatters/excel_formatter.py

"""
비플로우 분석 결과를 엑셀 포맷으로 변환하는 모듈
HTML과 유사한 레이아웃으로 엑셀 시트 생성
"""
import pandas as pd
import numpy as np
from pathlib import Path
import webbrowser

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
            workbook = writer.book
            
            # 리포트 시트와 대시보드 시트 생성
            self._create_report_sheet(writer, template_vars)
            self._create_dashboard_sheet(writer, template_vars)
            
            # 작성기 저장 및 닫기
            writer.close()
            
            return output_path
            
        except Exception as e:
            print(f"엑셀 파일 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_report_sheet(self, writer, template_vars):
        """HTML 리포트와 유사한 레이아웃의 시트 생성"""
        # 워크시트 생성
        worksheet = writer.book.add_worksheet('리포트')
        
        # 헤더 스타일
        header_format = writer.book.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#f0f0f0',
            'border': 1
        })
        
        # 섹션 제목 스타일
        section_format = writer.book.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left',
            'bg_color': '#e0e0ff',
            'border': 1
        })
        
        # 일반 텍스트 스타일
        text_format = writer.book.add_format({
            'font_size': 11,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        # 인사이트 블록 스타일
        insight_format = writer.book.add_format({
            'font_size': 11,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True,
            'bg_color': '#f9f9f9',
            'border_color': '#007bff',
            'left': 5,
            'border': 1
        })

        # 타이틀
        title = template_vars.get('title', '엔트리 셀러 인사이트 리포트')
        worksheet.merge_range('A1:G1', title, header_format)
        
        # 기본 정보
        worksheet.write('A2', '생성일시:', text_format)
        worksheet.write('B2', template_vars.get('timestamp', ''), text_format)
        worksheet.write('A3', '분석 기간:', text_format)
        worksheet.write('B3', template_vars.get('period', '알 수 없음'), text_format)
        worksheet.write('A4', '샘플 수:', text_format)
        worksheet.write('B4', f"{template_vars.get('total_orders', 0)}건", text_format)
        
        # 첫 번째 섹션: 요약 인사이트
        current_row = 6
        worksheet.merge_range(f'A{current_row}:G{current_row}', '1. 요약 인사이트', section_format)
        current_row += 1
        
        # 요약 인사이트 목록
        if 'summary_insights' in template_vars:
            for i, insight in enumerate(template_vars['summary_insights']):
                worksheet.merge_range(f'A{current_row}:G{current_row}', f"• {insight}", insight_format)
                current_row += 1
        else:
            worksheet.merge_range(f'A{current_row}:G{current_row}', "요약 데이터가 없습니다.", text_format)
            current_row += 1
        
        current_row += 1  # 여백
        
        # 두 번째 섹션: 자동 추출 키워드 분석
        worksheet.merge_range(f'A{current_row}:G{current_row}', '2. 자동 추출 키워드 분석', section_format)
        current_row += 1
        
        if template_vars.get('has_auto_keywords', False):
            # 스타일 키워드
            if template_vars.get('has_style_keywords', False):
                style_keywords = template_vars.get('style_keywords', [])
                worksheet.write(f'A{current_row}', '스타일 키워드:', text_format)
                worksheet.merge_range(f'B{current_row}:G{current_row}', ', '.join(style_keywords), text_format)
                current_row += 1
            
            # 상품 키워드
            if template_vars.get('has_product_keywords', False):
                product_keywords = [item['keyword'] for item in template_vars.get('product_keywords', [])]
                worksheet.write(f'A{current_row}', '상품 키워드:', text_format)
                worksheet.merge_range(f'B{current_row}:G{current_row}', ', '.join(product_keywords), text_format)
                current_row += 1
            
            # 색상 그룹
            if template_vars.get('has_color_groups', False):
                color_groups = [item['color'] for item in template_vars.get('color_groups', [])]
                worksheet.write(f'A{current_row}', '주요 색상 그룹:', text_format)
                worksheet.merge_range(f'B{current_row}:G{current_row}', ', '.join(color_groups), text_format)
                current_row += 1
            
            # 자동 인사이트
            if 'auto_insights' in template_vars and template_vars['auto_insights']:
                current_row += 1
                for insight in template_vars['auto_insights']:
                    worksheet.merge_range(f'A{current_row}:G{current_row}', insight['text'], insight_format)
                    current_row += 1
        else:
            worksheet.merge_range(f'A{current_row}:G{current_row}', "키워드 데이터가 충분치 않습니다.", text_format)
            current_row += 1
        
        current_row += 1  # 여백
        
        # 세 번째 섹션: 전략 가이드
        worksheet.merge_range(f'A{current_row}:G{current_row}', '3. 전략 가이드', section_format)
        current_row += 1
        
        if template_vars.get('has_strategy', False):
            # 추천 상품 구성
            if 'recommended_products' in template_vars and template_vars['recommended_products']:
                worksheet.write(f'A{current_row}', '추천 상품 구성:', text_format)
                worksheet.merge_range(f'B{current_row}:G{current_row}', ', '.join(template_vars['recommended_products']), text_format)
                current_row += 1
            
            # 주력 가격대
            if 'main_price_range' in template_vars:
                worksheet.write(f'A{current_row}', '주력 가격대:', text_format)
                price_info = f"{template_vars['main_price_range']} (약 {template_vars.get('main_price_percent', 0)}% 비중)"
                worksheet.merge_range(f'B{current_row}:G{current_row}', price_info, text_format)
                current_row += 1
            
            # 우선 판매 채널
            if 'has_channels' in template_vars and template_vars['has_channels']:
                worksheet.write(f'A{current_row}', '우선 판매 채널:', text_format)
                worksheet.merge_range(f'B{current_row}:G{current_row}', template_vars.get('top_channels', '데이터 없음'), text_format)
                current_row += 1
            
            # 추가 키워드 추천
            if 'keyword_recommendations' in template_vars and template_vars['keyword_recommendations']:
                worksheet.write(f'A{current_row}', '추가 키워드 추천:', text_format)
                # 여기서는 단순히 문자열 리스트를 합쳐 쓰는 방식
                worksheet.merge_range(f'B{current_row}:G{current_row}', ', '.join(template_vars['keyword_recommendations']), text_format)
                current_row += 1
            
            current_row += 1
            worksheet.merge_range(f'A{current_row}:G{current_row}', "위 전략을 토대로 상품명, 상세설명, 프로모션 기획 등을 진행해보세요.", text_format)
            current_row += 1
        else:
            worksheet.merge_range(f'A{current_row}:G{current_row}', "전략 정보가 없습니다.", text_format)
            current_row += 1
        
        # 컬럼 너비 설정
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:G', 20)
    
    def _create_dashboard_sheet(self, writer, template_vars):
        """HTML 대시보드와 유사한 레이아웃의 시트 생성"""
        # 워크시트 생성
        worksheet = writer.book.add_worksheet('대시보드')
        
        # 헤더 스타일
        header_format = writer.book.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#ffffff',
            'border': 1
        })
        
        # 차트 제목 스타일
        chart_title_format = writer.book.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        # 인사이트 스타일
        insight_format = writer.book.add_format({
            'font_size': 11,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True,
            'bg_color': '#e9f7fe',
            'border': 1
        })
        
        # 가이드 제목 스타일
        guide_title_format = writer.book.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#f0f8ff',
            'border': 1
        })
        
        # 가이드 항목 스타일
        guide_item_format = writer.book.add_format({
            'font_size': 11,
            'align': 'left',
            'valign': 'vcenter',
            'bg_color': '#ffffff',
            'border': 1
        })
        
        # 타이틀
        title = template_vars.get('title', '엔트리 셀러 인사이트 대시보드')
        worksheet.merge_range('A1:H1', title, header_format)
        worksheet.write('A2', template_vars.get('subtitle', ''), writer.book.add_format({'align': 'center'}))
        
        # 차트 데이터를 시트에 추가하고 차트 생성
        current_row = 4
        
        # 첫째 줄: 상품 유형 차트
        if 'product_data' in template_vars:
            worksheet.merge_range(f'A{current_row}:D{current_row}', '인기 상품 유형 TOP5', chart_title_format)
            current_row += 1
            
            # 데이터 작성
            product_data = template_vars['product_data']
            worksheet.write(f'A{current_row}', '상품 유형', writer.book.add_format({'bold': True}))
            worksheet.write(f'B{current_row}', '빈도', writer.book.add_format({'bold': True}))
            current_row += 1
            
            start_row = current_row
            for i, item in enumerate(product_data[:5]):  # Top 5만 표시
                worksheet.write(f'A{current_row}', item['name'])
                worksheet.write(f'B{current_row}', item['value'])
                current_row += 1
            
            # 차트 생성
            chart = writer.book.add_chart({'type': 'bar'})
            chart.add_series({
                'name': '빈도',
                'categories': [worksheet.name, start_row, 0, current_row-1, 0],
                'values': [worksheet.name, start_row, 1, current_row-1, 1],
                'fill': {'color': '#0088FE'}
            })
            chart.set_title({'name': '인기 상품 유형'})
            chart.set_legend({'none': True})
            chart.set_y_axis({'reverse': True})  # 역순으로 표시
            worksheet.insert_chart(f'C{start_row}', chart, {'x_scale': 1.2, 'y_scale': 1.5})
            
            # 인사이트 추가
            current_row += 1
            if 'product_insight' in template_vars:
                worksheet.merge_range(f'A{current_row}:D{current_row}', f"인사이트: {template_vars['product_insight']}", insight_format)
            
            current_row += 8  # 차트 공간 확보
        
        # 색상 차트 (오른쪽)
        if 'color_data' in template_vars:
            right_col = 'E'
            color_row = 4
            
            worksheet.merge_range(f'{right_col}{color_row}:H{color_row}', '인기 색상 TOP5', chart_title_format)
            color_row += 1
            
            # 데이터 작성
            color_data = template_vars['color_data']
            worksheet.write(f'{right_col}{color_row}', '색상', writer.book.add_format({'bold': True}))
            worksheet.write(f'{chr(ord(right_col)+1)}{color_row}', '빈도', writer.book.add_format({'bold': True}))
            color_row += 1
            
            start_row = color_row
            for i, item in enumerate(color_data[:5]):  # Top 5만 표시
                worksheet.write(f'{right_col}{color_row}', item['name'])
                worksheet.write(f'{chr(ord(right_col)+1)}{color_row}', item['value'])
                color_row += 1
            
            # 차트 생성
            chart = writer.book.add_chart({'type': 'pie'})
            chart.add_series({
                'name': '색상 분포',
                'categories': [worksheet.name, start_row, ord(right_col)-ord('A'), color_row-1, ord(right_col)-ord('A')],
                'values': [worksheet.name, start_row, ord(right_col)-ord('A')+1, color_row-1, ord(right_col)-ord('A')+1],
                'data_labels': {'percentage': True},
                'points': [
                    {'fill': {'color': '#0088FE'}},
                    {'fill': {'color': '#00C49F'}},
                    {'fill': {'color': '#FFBB28'}},
                    {'fill': {'color': '#FF8042'}},
                    {'fill': {'color': '#8884d8'}}
                ]
            })
            chart.set_title({'name': '인기 색상'})
            worksheet.insert_chart(f'{chr(ord(right_col)+2)}{start_row}', chart, {'x_scale': 1.2, 'y_scale': 1.5})
            
            # 인사이트 추가
            color_row += 1
            if 'color_insight' in template_vars:
                worksheet.merge_range(f'{right_col}{color_row}:H{color_row}', f"인사이트: {template_vars['color_insight']}", insight_format)
        
        # 두번째 줄: 가격대 차트 + 채널 차트
        price_row = current_row + 2
        if 'price_data' in template_vars:
            worksheet.merge_range(f'A{price_row}:D{price_row}', '가격대별 상품 분포', chart_title_format)
            price_row += 1
            
            # 데이터 작성
            price_data = template_vars['price_data']
            worksheet.write(f'A{price_row}', '가격대', writer.book.add_format({'bold': True}))
            worksheet.write(f'B{price_row}', '상품 수', writer.book.add_format({'bold': True}))
            worksheet.write(f'C{price_row}', '비율(%)', writer.book.add_format({'bold': True}))
            price_row += 1
            
            start_row = price_row
            for i, item in enumerate(price_data[:6]):  # 상위 6개만 표시
                worksheet.write(f'A{price_row}', item['name'])
                worksheet.write(f'B{price_row}', item['value'])
                worksheet.write(f'C{price_row}', item.get('percent', 0))
                price_row += 1
            
            # 차트 생성
            chart = writer.book.add_chart({'type': 'column'})
            chart.add_series({
                'name': '상품 수',
                'categories': [worksheet.name, start_row, 0, price_row-1, 0],
                'values': [worksheet.name, start_row, 1, price_row-1, 1],
                'fill': {'color': '#00C49F'}
            })
            chart.set_title({'name': '가격대별 상품 분포'})
            chart.set_legend({'none': True})
            worksheet.insert_chart(f'A{price_row+1}', chart, {'x_scale': 1.5, 'y_scale': 1.5})
            
            # 인사이트 추가
            price_row += 10  # 차트 공간 확보
            if 'price_insight' in template_vars:
                worksheet.merge_range(f'A{price_row}:D{price_row}', f"인사이트: {template_vars['price_insight']}", insight_format)
        
        # 채널 차트 (오른쪽)
        if 'channel_data' in template_vars:
            right_col = 'E'
            channel_row = price_row - 12  # 가격 차트와 유사한 높이를 맞추려 한 듯
            
            worksheet.merge_range(f'{right_col}{channel_row}:H{channel_row}', '주요 판매 채널', chart_title_format)
            channel_row += 1
            
            # 데이터 작성
            channel_data = template_vars['channel_data']
            worksheet.write(f'{right_col}{channel_row}', '판매 채널', writer.book.add_format({'bold': True}))
            worksheet.write(f'{chr(ord(right_col)+1)}{channel_row}', '주문 수', writer.book.add_format({'bold': True}))
            channel_row += 1
            
            start_row = channel_row
            for i, item in enumerate(channel_data[:5]):  # Top 5만 표시
                worksheet.write(f'{right_col}{channel_row}', item['name'])
                worksheet.write(f'{chr(ord(right_col)+1)}{channel_row}', item['value'])
                channel_row += 1
            
            # 차트 생성
            chart = writer.book.add_chart({'type': 'column'})
            chart.add_series({
                'name': '주문 수',
                'categories': [worksheet.name, start_row, ord(right_col)-ord('A'), channel_row-1, ord(right_col)-ord('A')],
                'values': [worksheet.name, start_row, ord(right_col)-ord('A')+1, channel_row-1, ord(right_col)-ord('A')+1],
                'fill': {'color': '#FFBB28'}
            })
            chart.set_title({'name': '주요 판매 채널'})
            chart.set_legend({'none': True})
            worksheet.insert_chart(f'{right_col}{channel_row+1}', chart, {'x_scale': 1.5, 'y_scale': 1.5})
            
            # 인사이트 추가
            channel_row += 10  # 차트 공간 확보
            if 'channel_insight' in template_vars:
                worksheet.merge_range(f'{right_col}{channel_row}:H{channel_row}', f"인사이트: {template_vars['channel_insight']}", insight_format)
        
        # 기존에는 guide_row = price_row + 3 였으나, 색상/채널 병합구간과 겹쳐
        # 에러가 났으므로 조금 더 아래로 (여유롭게 +15) 잡아 겹침을 피함.
        guide_row = price_row + 15
        
        worksheet.merge_range(f'A{guide_row}:H{guide_row}', '엔트리 셀러를 위한 핵심 실행 가이드', guide_title_format)
        guide_row += 1
        
        # (1) 추천 상품 구성
        if 'product_recommendations' in template_vars:
            worksheet.merge_range(f'A{guide_row}:B{guide_row}', '추천 상품 구성', writer.book.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
            guide_row += 1
            for item in template_vars.get('product_recommendations', []):
                worksheet.write(f'A{guide_row}', f"• {item.get('name', '')}", guide_item_format)
                worksheet.write(f'B{guide_row}', item.get('description', ''), guide_item_format)
                guide_row += 1
        
        guide_row += 2  # 섹션 간격 띄우기
        
        # (2) 채널 & 가격 전략
        if 'channel_recommendations' in template_vars:
            worksheet.merge_range(f'A{guide_row}:B{guide_row}', '채널 & 가격 전략', writer.book.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
            guide_row += 1
            for item in template_vars.get('channel_recommendations', []):
                worksheet.write(f'A{guide_row}', f"• {item.get('name', '')}", guide_item_format)
                worksheet.write(f'B{guide_row}', item.get('description', ''), guide_item_format)
                guide_row += 1
        
        guide_row += 2
        
        # (3) 핵심 키워드
        if 'keyword_recommendations' in template_vars and template_vars['keyword_recommendations']:
            worksheet.merge_range(f'A{guide_row}:B{guide_row}', '핵심 키워드', writer.book.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
            guide_row += 1
            # 여기서는 문자열 리스트로 가정해서 처리
            for kw in template_vars['keyword_recommendations']:
                worksheet.write(f'A{guide_row}', f"• {kw}", guide_item_format)
                worksheet.write(f'B{guide_row}', "", guide_item_format)
                guide_row += 1
        
        # 컬럼 너비 설정
        worksheet.set_column('A:H', 18)
