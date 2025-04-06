# output/formatters/excel_formatter/sheets/report_sheet.py
"""
리포트 시트 생성 로직
"""
import pandas as pd

def create_report_sheet(writer, template_vars):
    """
    HTML 리포트와 유사한 레이아웃의 시트 생성
    """
    workbook = writer.book
    worksheet = workbook.add_worksheet('리포트')

    # 헤더 스타일
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#f0f0f0',
        'border': 1
    })

    # 섹션 제목 스타일
    section_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'left',
        'bg_color': '#e0e0ff',
        'border': 1
    })

    # 일반 텍스트 스타일
    text_format = workbook.add_format({
        'font_size': 11,
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True
    })

    # 인사이트 블록 스타일
    insight_format = workbook.add_format({
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
