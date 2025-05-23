# output/formatters/excel_formatter/sheets/dashboard_sheet.py
"""
대시보드 시트 생성 로직 - 차트 크기가 조정된 HTML 스타일 그리드 레이아웃
"""
import pandas as pd

def create_dashboard_sheet(writer, template_vars):
    """
    HTML과 유사한 2x3 그리드 레이아웃으로 대시보드 생성
    각 표 아래에 관련 차트가 배치되고, 차트들이 서로 겹치지 않도록 크기 조정
    """
    workbook = writer.book
    worksheet = workbook.add_worksheet('대시보드')

    # 스타일 정의
    header_format = workbook.add_format({
        'bold': True, 'font_size': 16, 'align': 'center', 
        'valign': 'vcenter', 'bg_color': '#ffffff', 'border': 1
    })
    
    chart_title_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
    })
    
    insight_format = workbook.add_format({
        'font_size': 11, 'align': 'left', 'valign': 'vcenter',
        'text_wrap': True, 'bg_color': '#e9f7fe', 'border': 1
    })
    
    guide_title_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'align': 'center',
        'valign': 'vcenter', 'bg_color': '#f0f8ff', 'border': 1
    })
    
    guide_item_format = workbook.add_format({
        'font_size': 11, 'align': 'left', 'valign': 'vcenter', 
        'bg_color': '#ffffff', 'border': 1
    })
    
    text_format = workbook.add_format({
        'font_size': 11, 'align': 'left', 'valign': 'vcenter'
    })
    
    bold_format = workbook.add_format({
        'bold': True, 'font_size': 11
    })

    # 열 너비 설정 - 균등하게 분배하여 겹침 방지
    for col in range(8):  # A부터 H까지
        worksheet.set_column(col, col, 12)  # 모든 열을 12 단위로 통일

    # 타이틀
    title = template_vars.get('title', '엔트리 셀러 인사이트 대시보드')
    worksheet.merge_range('A1:H1', title, header_format)
    worksheet.merge_range('A2:H2', template_vars.get('subtitle', ''), workbook.add_format({'align': 'center'}))

    # 섹션 간 간격 확보를 위한 그리드 정의 (2x4 그리드)
    grid = {
        # 왼쪽 상단 - 인기 상품 유형
        'A': {'title_cell': 'A4:D4', 'data_start': 'A5', 'chart_cell': 'A11', 'insight_cell': 'A22:D22'},
        
        # 오른쪽 상단 - 인기 색상
        'B': {'title_cell': 'E4:H4', 'data_start': 'E5', 'chart_cell': 'E11', 'insight_cell': 'E22:H22'},
        
        # 왼쪽 중단 - 가격대별 상품 분포
        'C': {'title_cell': 'A24:D24', 'data_start': 'A25', 'chart_cell': 'A31', 'insight_cell': 'A42:D42'},
        
        # 오른쪽 중단 - 주요 판매 채널
        'D': {'title_cell': 'E24:H24', 'data_start': 'E25', 'chart_cell': 'E31', 'insight_cell': 'E42:H42'},
        
        # 왼쪽 하단 - 인기 소재
        'E': {'title_cell': 'A44:D44', 'data_start': 'A45', 'chart_cell': 'A51', 'insight_cell': 'A62:D62'},
        
        # 오른쪽 하단 - 인기 디자인
        'F': {'title_cell': 'E44:H44', 'data_start': 'E45', 'chart_cell': 'E51', 'insight_cell': 'E62:H62'}
    }

    # 차트 크기를 더 작게 조정하여 겹침 방지
    chart_scale = {'x_scale': 1.2, 'y_scale': 1.1}

    # 1. 인기 상품 유형 (왼쪽 상단 - A)
    if 'product_data' in template_vars:
        worksheet.merge_range(grid['A']['title_cell'], '인기 상품 유형 TOP5', chart_title_format)
        row = int(grid['A']['data_start'][1:])
        worksheet.write(f'A{row}', '상품 유형', bold_format)
        worksheet.write(f'B{row}', '빈도', bold_format)
        product_data = template_vars['product_data']
        for i, item in enumerate(product_data[:5]):
            row = int(grid['A']['data_start'][1:]) + i + 1
            worksheet.write(f'A{row}', item['name'], text_format)
            worksheet.write(f'B{row}', item['value'], text_format)
        chart = workbook.add_chart({'type': 'bar'})
        chart.add_series({
            'name': '빈도',
            'categories': [worksheet.name, int(grid['A']['data_start'][1:]), 0, int(grid['A']['data_start'][1:]) + min(len(product_data), 5), 0],
            'values': [worksheet.name, int(grid['A']['data_start'][1:]), 1, int(grid['A']['data_start'][1:]) + min(len(product_data), 5), 1],
            'fill': {'color': '#0088FE'}
        })
        chart.set_title({'name': '인기 상품 유형'})
        chart.set_legend({'none': True})
        chart.set_y_axis({'reverse': True})
        worksheet.insert_chart(grid['A']['chart_cell'], chart, chart_scale)
        if 'product_insight' in template_vars:
            worksheet.merge_range(grid['A']['insight_cell'], f"인사이트: {template_vars['product_insight']}", insight_format)

    # 2. 인기 색상 (오른쪽 상단 - B)
    if 'color_data' in template_vars:
        worksheet.merge_range(grid['B']['title_cell'], '인기 색상 TOP5', chart_title_format)
        row = int(grid['B']['data_start'][1:])
        worksheet.write(f'E{row}', '색상', bold_format)
        worksheet.write(f'F{row}', '빈도', bold_format)
        color_data = template_vars['color_data']
        for i, item in enumerate(color_data[:5]):
            row = int(grid['B']['data_start'][1:]) + i + 1
            worksheet.write(f'E{row}', item['name'], text_format)
            worksheet.write(f'F{row}', item['value'], text_format)
        chart = workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name': '색상 분포',
            'categories': [worksheet.name, int(grid['B']['data_start'][1:]), 4, int(grid['B']['data_start'][1:]) + min(len(color_data), 5), 4],
            'values': [worksheet.name, int(grid['B']['data_start'][1:]), 5, int(grid['B']['data_start'][1:]) + min(len(color_data), 5), 5],
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
        worksheet.insert_chart(grid['B']['chart_cell'], chart, chart_scale)
        if 'color_insight' in template_vars:
            worksheet.merge_range(grid['B']['insight_cell'], f"인사이트: {template_vars['color_insight']}", insight_format)

    # 3. 가격대별 상품 분포 (왼쪽 중단 - C)
    if 'price_data' in template_vars:
        worksheet.merge_range(grid['C']['title_cell'], '가격대별 상품 분포', chart_title_format)
        row = int(grid['C']['data_start'][1:])
        worksheet.write(f'A{row}', '가격대', bold_format)
        worksheet.write(f'B{row}', '상품 수', bold_format)
        worksheet.write(f'C{row}', '비율(%)', bold_format)
        price_data = template_vars['price_data']
        for i, item in enumerate(price_data[:5]):
            row = int(grid['C']['data_start'][1:]) + i + 1
            worksheet.write(f'A{row}', item['name'], text_format)
            worksheet.write(f'B{row}', item['value'], text_format)
            worksheet.write(f'C{row}', item.get('percent', 0), text_format)
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '상품 수',
            'categories': [worksheet.name, int(grid['C']['data_start'][1:]), 0, int(grid['C']['data_start'][1:]) + min(len(price_data), 5), 0],
            'values': [worksheet.name, int(grid['C']['data_start'][1:]), 1, int(grid['C']['data_start'][1:]) + min(len(price_data), 5), 1],
            'fill': {'color': '#00C49F'}
        })
        chart.set_title({'name': '가격대별 상품 분포'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(grid['C']['chart_cell'], chart, chart_scale)
        if 'price_insight' in template_vars:
            worksheet.merge_range(grid['C']['insight_cell'], f"인사이트: {template_vars['price_insight']}", insight_format)

    # 4. 주요 판매 채널 (오른쪽 중단 - D)
    if 'channel_data' in template_vars:
        worksheet.merge_range(grid['D']['title_cell'], '주요 판매 채널', chart_title_format)
        row = int(grid['D']['data_start'][1:])
        worksheet.write(f'E{row}', '판매 채널', bold_format)
        worksheet.write(f'F{row}', '주문 수', bold_format)
        channel_data = template_vars['channel_data']
        for i, item in enumerate(channel_data[:5]):
            row = int(grid['D']['data_start'][1:]) + i + 1
            worksheet.write(f'E{row}', item['name'], text_format)
            worksheet.write(f'F{row}', item['value'], text_format)
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '주문 수',
            'categories': [worksheet.name, int(grid['D']['data_start'][1:]), 4, int(grid['D']['data_start'][1:]) + min(len(channel_data), 5), 4],
            'values': [worksheet.name, int(grid['D']['data_start'][1:]), 5, int(grid['D']['data_start'][1:]) + min(len(channel_data), 5), 5],
            'fill': {'color': '#FFBB28'}
        })
        chart.set_title({'name': '주요 판매 채널'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(grid['D']['chart_cell'], chart, chart_scale)
        if 'channel_insight' in template_vars:
            worksheet.merge_range(grid['D']['insight_cell'], f"인사이트: {template_vars['channel_insight']}", insight_format)

    # 5. 인기 소재 (왼쪽 하단 - E)
    if 'material_data' in template_vars:
        worksheet.merge_range(grid['E']['title_cell'], '인기 소재', chart_title_format)
        row = int(grid['E']['data_start'][1:])
        worksheet.write(f'A{row}', '소재', bold_format)
        worksheet.write(f'B{row}', '빈도', bold_format)
        material_data = template_vars['material_data']
        for i, item in enumerate(material_data[:5]):
            row = int(grid['E']['data_start'][1:]) + i + 1
            worksheet.write(f'A{row}', item['name'], text_format)
            worksheet.write(f'B{row}', item['value'], text_format)
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '빈도',
            'categories': [worksheet.name, int(grid['E']['data_start'][1:]), 0, int(grid['E']['data_start'][1:]) + min(len(material_data), 5), 0],
            'values': [worksheet.name, int(grid['E']['data_start'][1:]), 1, int(grid['E']['data_start'][1:]) + min(len(material_data), 5), 1],
            'fill': {'color': '#8884d8'}
        })
        chart.set_title({'name': '인기 소재'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(grid['E']['chart_cell'], chart, chart_scale)
        if 'material_insight' in template_vars:
            worksheet.merge_range(grid['E']['insight_cell'], f"인사이트: {template_vars['material_insight']}", insight_format)

    # 6. 인기 디자인 (오른쪽 하단 - F)
    if 'design_data' in template_vars:
        worksheet.merge_range(grid['F']['title_cell'], '인기 디자인 요소', chart_title_format)
        row = int(grid['F']['data_start'][1:])
        worksheet.write(f'E{row}', '디자인', bold_format)
        worksheet.write(f'F{row}', '빈도', bold_format)
        design_data = template_vars['design_data']
        for i, item in enumerate(design_data[:5]):
            row = int(grid['F']['data_start'][1:]) + i + 1
            worksheet.write(f'E{row}', item['name'], text_format)
            worksheet.write(f'F{row}', item['value'], text_format)
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': '빈도',
            'categories': [worksheet.name, int(grid['F']['data_start'][1:]), 4, int(grid['F']['data_start'][1:]) + min(len(design_data), 5), 4],
            'values': [worksheet.name, int(grid['F']['data_start'][1:]), 5, int(grid['F']['data_start'][1:]) + min(len(design_data), 5), 5],
            'fill': {'color': '#82ca9d'}
        })
        chart.set_title({'name': '인기 디자인 요소'})
        chart.set_legend({'none': True})
        worksheet.insert_chart(grid['F']['chart_cell'], chart, chart_scale)
        if 'design_insight' in template_vars:
            worksheet.merge_range(grid['F']['insight_cell'], f"인사이트: {template_vars['design_insight']}", insight_format)

    # 7. 사이즈 분포 (하단에 배치)
    if 'size_data' in template_vars:
        # 제목
        worksheet.merge_range('A64:D64', '사이즈 분포', chart_title_format)
        
        # 데이터 헤더
        row = 65
        worksheet.write(f'A{row}', '사이즈', bold_format)
        worksheet.write(f'B{row}', '빈도', bold_format)
        
        # 데이터 표
        size_data = template_vars['size_data']
        for i, item in enumerate(size_data[:5]):
            row = 65 + i + 1
            worksheet.write(f'A{row}', item['name'], text_format)
            worksheet.write(f'B{row}', item['value'], text_format)
        
        # 차트 (표 아래에 배치)
        chart = workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name': '사이즈 분포',
            'categories': [worksheet.name, 65, 0, 65 + min(len(size_data), 5), 0],
            'values': [worksheet.name, 65, 1, 65 + min(len(size_data), 5), 1],
            'data_labels': {'percentage': True},
            'points': [
                {'fill': {'color': '#0088FE'}},
                {'fill': {'color': '#00C49F'}},
                {'fill': {'color': '#FFBB28'}},
                {'fill': {'color': '#FF8042'}},
                {'fill': {'color': '#8884d8'}}
            ]
        })
        chart.set_title({'name': '사이즈 분포'})
        worksheet.insert_chart('A71', chart, chart_scale)
        
        # 인사이트
        if 'size_insight' in template_vars:
            worksheet.merge_range('A82:D82', f"인사이트: {template_vars['size_insight']}", insight_format)

    # 8. 베스트셀러 상품 (우측 하단에 배치)
    if 'bestseller_data' in template_vars:
        # 제목
        worksheet.merge_range('E64:H64', '베스트셀러 상품', chart_title_format)
        
        # 데이터 헤더
        row = 65
        worksheet.write(f'E{row}', '상품명', bold_format)
        worksheet.write(f'F{row}', '주문 수', bold_format)
        
        # 데이터 표
        bestseller_data = template_vars['bestseller_data']
        for i, item in enumerate(bestseller_data[:10]):
            row = 65 + i + 1
            worksheet.write(f'E{row}', item['name'], text_format)
            worksheet.write(f'F{row}', item['value'], text_format)
        
        # 차트 (표 아래에 배치)
        chart = workbook.add_chart({'type': 'bar'})
        chart.add_series({
            'name': '주문 수',
            'categories': [worksheet.name, 65, 4, 65 + min(len(bestseller_data), 10), 4],
            'values': [worksheet.name, 65, 5, 65 + min(len(bestseller_data), 10), 5],
            'fill': {'color': '#FF8042'}
        })
        chart.set_title({'name': '베스트셀러 상품'})
        chart.set_legend({'none': True})
        chart.set_y_axis({'reverse': True})
        worksheet.insert_chart('E76', chart, {'x_scale': 1.5, 'y_scale': 1.5})

    # 9. 실행 가이드 (하단)
    guide_row = 84  # 차트와 인사이트 다음 행부터 시작
    worksheet.merge_range(f'A{guide_row}:H{guide_row}', '엔트리 셀러를 위한 핵심 실행 가이드', guide_title_format)
    guide_row += 1

    # (1) 추천 상품 구성
    if 'product_recommendations' in template_vars:
        worksheet.merge_range(f'A{guide_row}:C{guide_row}', '추천 상품 구성', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        guide_row += 1
        for item in template_vars.get('product_recommendations', []):
            worksheet.write(f'A{guide_row}', f"• {item.get('name', '')}", guide_item_format)
            worksheet.merge_range(f'B{guide_row}:C{guide_row}', item.get('description', ''), guide_item_format)
            guide_row += 1

    # (2) 채널 & 가격 전략
    channel_row = 86  # 첫 번째 가이드와 같은 행에서 시작
    if 'channel_recommendations' in template_vars:
        worksheet.merge_range(f'E{channel_row}:G{channel_row}', '채널 & 가격 전략', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        channel_row += 1
        for item in template_vars.get('channel_recommendations', []):
            worksheet.write(f'E{channel_row}', f"• {item.get('name', '')}", guide_item_format)
            worksheet.merge_range(f'F{channel_row}:G{channel_row}', item.get('description', ''), guide_item_format)
            channel_row += 1

    # (3) 핵심 키워드
    guide_row = max(guide_row, channel_row) + 2  # 이전 두 가이드 중 더 긴 것 다음에 배치
    if 'keyword_recommendations' in template_vars and template_vars['keyword_recommendations']:
        worksheet.merge_range(f'A{guide_row}:D{guide_row}', '핵심 키워드', workbook.add_format({'bold': True, 'bg_color': '#f8f9fa'}))
        guide_row += 1
        
        kw_column_a = []
        kw_column_b = []
        
        # 키워드를 두 열로 분할
        keywords = template_vars['keyword_recommendations']
        half = len(keywords) // 2 + len(keywords) % 2
        kw_column_a = keywords[:half]
        kw_column_b = keywords[half:] if half < len(keywords) else []
        
        # 첫 번째 열 키워드
        for i, kw in enumerate(kw_column_a):
            # 이 부분을 수정 - 문자열과 딕셔너리 모두 처리
            if isinstance(kw, dict):
                worksheet.write(f'A{guide_row + i}', f"• {kw.get('name', '')}", guide_item_format)
                worksheet.write(f'B{guide_row + i}', kw.get('description', ''), guide_item_format)
            else:
                worksheet.write(f'A{guide_row + i}', f"• {kw}", guide_item_format)
                worksheet.write(f'B{guide_row + i}', "", guide_item_format)
        
        # 두 번째 열 키워드
        for i, kw in enumerate(kw_column_b):
            # 이 부분도 수정 - 문자열과 딕셔너리 모두 처리
            if isinstance(kw, dict):
                worksheet.write(f'C{guide_row + i}', f"• {kw.get('name', '')}", guide_item_format)
                worksheet.write(f'D{guide_row + i}', kw.get('description', ''), guide_item_format)
            else:
                worksheet.write(f'C{guide_row + i}', f"• {kw}", guide_item_format)
                worksheet.write(f'D{guide_row + i}', "", guide_item_format)

    # 행 높이 설정 - 차트 배치를 위한 공간 확보
    # 모든 행에 기본 높이 적용
    for i in range(4, 100):
        worksheet.set_row(i-1, 18)  # 기본 행 높이
    
    # 차트 영역은 충분한 높이 확보
    for i in range(11, 22):
        worksheet.set_row(i-1, 20)  # 차트 행 높이 증가
    
    for i in range(31, 42):
        worksheet.set_row(i-1, 20)  # 차트 행 높이 증가
    
    for i in range(51, 62):
        worksheet.set_row(i-1, 20)  # 차트 행 높이 증가
    
    for i in range(71, 82):
        worksheet.set_row(i-1, 20)  # 차트 행 높이 증가
    
    worksheet.set_row(0, 30)  # 타이틀 행 높이