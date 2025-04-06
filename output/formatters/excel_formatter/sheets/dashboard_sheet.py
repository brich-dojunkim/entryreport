# output/formatters/excel_formatter/sheets/dashboard_sheet.py
"""
대시보드 시트 생성 로직
"""
import pandas as pd

def create_dashboard_sheet(writer, template_vars):
    """
    HTML 대시보드와 유사한 레이아웃의 시트 생성
    """
    workbook = writer.book
    worksheet = workbook.add_worksheet('대시보드')

    # 헤더 스타일
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#ffffff',
        'border': 1
    })

    # 차트 제목 스타일
    chart_title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })

    # 인사이트 스타일
    insight_format = workbook.add_format({
        'font_size': 11,
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True,
        'bg_color': '#e9f7fe',
        'border': 1
    })

    # 가이드 제목 스타일
    guide_title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#f0f8ff',
        'border': 1
    })

    # 가이드 항목 스타일
    guide_item_format = workbook.add_format({
        'font_size': 11,
        'align': 'left',
        'valign': 'vcenter',
        'bg_color': '#ffffff',
        'border': 1
    })

    # 타이틀
    title = template_vars.get('title', '엔트리 셀러 인사이트 대시보드')
    worksheet.merge_range('A1:H1', title, header_format)
    worksheet.write('A2', template_vars.get('subtitle', ''), workbook.add_format({'align': 'center'}))

    current_row = 4

    # ----------------------------
    # 1) 상품 유형 차트 (왼쪽 상단)
    # ----------------------------
    if 'product_data' in template_vars:
        worksheet.merge_range(f'A{current_row}:D{current_row}', '인기 상품 유형 TOP5', chart_title_format)
        current_row += 1

        product_data = template_vars['product_data']
        worksheet.write(f'A{current_row}', '상품 유형', workbook.add_format({'bold': True}))
        worksheet.write(f'B{current_row}', '빈도', workbook.add_format({'bold': True}))
        current_row += 1

        start_row = current_row
        for i, item in enumerate(product_data[:5]):
            worksheet.write(f'A{current_row}', item['name'])
            worksheet.write(f'B{current_row}', item['value'])
            current_row += 1

        chart = workbook.add_chart({'type': 'bar'})
        chart.add_series({
            'name': '빈도',
            'categories': [worksheet.name, start_row, 0, current_row-1, 0],
            'values': [worksheet.name, start_row, 1, current_row-1, 1],
            'fill': {'color': '#0088FE'}
        })
        chart.set_title({'name': '인기 상품 유형'})
        chart.set_legend({'none': True})
        chart.set_y_axis({'reverse': True})
        worksheet.insert_chart(f'C{start_row}', chart, {'x_scale': 1.2, 'y_scale': 1.5})

        current_row += 1
        if 'product_insight' in template_vars:
            worksheet.merge_range(f'A{current_row}:D{current_row}', f"인사이트: {template_vars['product_insight']}", insight_format)

        current_row += 8  # 차트 공간 확보

    # ----------------------------
    # 2) 색상 차트 (오른쪽 상단)
    # ----------------------------
    if 'color_data' in template_vars:
        right_col = 'E'
        color_row = 4

        worksheet.merge_range(f'{right_col}{color_row}:H{color_row}', '인기 색상 TOP5', chart_title_format)
        color_row += 1

        color_data = template_vars['color_data']
        worksheet.write(f'{right_col}{color_row}', '색상', workbook.add_format({'bold': True}))
        worksheet.write(f'{chr(ord(right_col)+1)}{color_row}', '빈도', workbook.add_format({'bold': True}))
        color_row += 1

        start_row = color_row
        for i, item in enumerate(color_data[:5]):
            worksheet.write(f'{right_col}{color_row}', item['name'])
            worksheet.write(f'{chr(ord(right_col)+1)}{color_row}', item['value'])
            color_row += 1

        chart = workbook.add_chart({'type': 'pie'})
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

        color_row += 1
        if 'color_insight' in template_vars:
            worksheet.merge_range(f'{right_col}{color_row}:H{color_row}', f"인사이트: {template_vars['color_insight']}", insight_format)

    # ----------------------------
    # 3) 가격대 차트 (왼쪽 하단)
    # ----------------------------
    price_row = current_row + 2
    if 'price_data' in template_vars:
        worksheet.merge_range(f'A{price_row}:D{price_row}', '가격대별 상품 분포', chart_title_format)
        price_row += 1

        price_data = template_vars['price_data']
        worksheet.write(f'A{price_row}', '가격대', workbook.add_format({'bold': True}))
        worksheet.write(f'B{price_row}', '상품 수', workbook.add_format({'bold': True}))
        worksheet.write(f'C{price_row}', '비율(%)', workbook.add_format({'bold': True}))
        price_row += 1

        start_row = price_row
        for i, item in enumerate(price_data[:6]):
            worksheet.write(f'A{price_row}', item['name'])
            worksheet.write(f'B{price_row}', item['value'])
            worksheet.write(f'C{price_row}', item.get('percent', 0))
            price_row += 1

        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '상품 수',
            'categories': [worksheet.name, start_row, 0, price_row-1, 0],
            'values': [worksheet.name, start_row, 1, price_row-1, 1],
            'fill': {'color': '#00C49F'}
        })
        chart.set_title({'name': '가격대별 상품 분포'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(f'A{price_row+1}', chart, {'x_scale': 1.5, 'y_scale': 1.5})

        price_row += 10
        if 'price_insight' in template_vars:
            worksheet.merge_range(f'A{price_row}:D{price_row}', f"인사이트: {template_vars['price_insight']}", insight_format)

    # ----------------------------
    # 4) 채널 차트 (오른쪽 하단)
    # ----------------------------
    if 'channel_data' in template_vars:
        right_col = 'E'
        channel_row = price_row - 12  # 기존 로직 유지

        worksheet.merge_range(f'{right_col}{channel_row}:H{channel_row}', '주요 판매 채널', chart_title_format)
        channel_row += 1

        channel_data = template_vars['channel_data']
        worksheet.write(f'{right_col}{channel_row}', '판매 채널', workbook.add_format({'bold': True}))
        worksheet.write(f'{chr(ord(right_col)+1)}{channel_row}', '주문 수', workbook.add_format({'bold': True}))
        channel_row += 1

        start_row = channel_row
        for i, item in enumerate(channel_data[:5]):
            worksheet.write(f'{right_col}{channel_row}', item['name'])
            worksheet.write(f'{chr(ord(right_col)+1)}{channel_row}', item['value'])
            channel_row += 1

        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '주문 수',
            'categories': [worksheet.name, start_row, ord(right_col)-ord('A'), channel_row-1, ord(right_col)-ord('A')],
            'values': [worksheet.name, start_row, ord(right_col)-ord('A')+1, channel_row-1, ord(right_col)-ord('A')+1],
            'fill': {'color': '#FFBB28'}
        })
        chart.set_title({'name': '주요 판매 채널'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(f'{right_col}{channel_row+1}', chart, {'x_scale': 1.5, 'y_scale': 1.5})

        channel_row += 10
        if 'channel_insight' in template_vars:
            worksheet.merge_range(f'{right_col}{channel_row}:H{channel_row}', f"인사이트: {template_vars['channel_insight']}", insight_format)

    # ----------------------------
    # 5) 실행 가이드
    # ----------------------------
    guide_row = price_row + 15
    worksheet.merge_range(f'A{guide_row}:H{guide_row}', '엔트리 셀러를 위한 핵심 실행 가이드', guide_title_format)
    guide_row += 1

    # (1) 추천 상품 구성
    if 'product_recommendations' in template_vars:
        worksheet.merge_range(f'A{guide_row}:B{guide_row}', '추천 상품 구성', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        guide_row += 1
        for item in template_vars.get('product_recommendations', []):
            worksheet.write(f'A{guide_row}', f"• {item.get('name', '')}", guide_item_format)
            worksheet.write(f'B{guide_row}', item.get('description', ''), guide_item_format)
            guide_row += 1

    guide_row += 2

    # (2) 채널 & 가격 전략
    if 'channel_recommendations' in template_vars:
        worksheet.merge_range(f'A{guide_row}:B{guide_row}', '채널 & 가격 전략', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        guide_row += 1
        for item in template_vars.get('channel_recommendations', []):
            worksheet.write(f'A{guide_row}', f"• {item.get('name', '')}", guide_item_format)
            worksheet.write(f'B{guide_row}', item.get('description', ''), guide_item_format)
            guide_row += 1

    guide_row += 2

    # (3) 핵심 키워드
    if 'keyword_recommendations' in template_vars and template_vars['keyword_recommendations']:
        worksheet.merge_range(f'A{guide_row}:B{guide_row}', '핵심 키워드', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        guide_row += 1
        for kw in template_vars['keyword_recommendations']:
            worksheet.write(f'A{guide_row}', f"• {kw}", guide_item_format)
            worksheet.write(f'B{guide_row}', "", guide_item_format)
            guide_row += 1

    # 컬럼 너비 설정
    worksheet.set_column('A:H', 18)
