import os
import time
import webbrowser
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from modules.chart_generator import ChartGenerator
from modules.insights_formatter import InsightsFormatter
from modules.base_generator import BaseGenerator

class DashboardGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 대시보드 생성"""
    
    def __init__(self, insights, output_folder='bflow_reports'):
        """
        대시보드 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - output_folder: 결과물 저장 폴더
        """
        # 부모 클래스 초기화
        super().__init__(insights, output_folder)
        
        # 템플릿 경로 설정
        self.template_folder = Path('templates')
        
        # 디버깅 정보 출력
        print(f"DashboardGenerator 초기화 - insights 타입: {type(insights)}")
        print(f"DashboardGenerator 초기화 - summary 타입: {type(self.summary)}")
    
    def _convert_to_serializable(self, data):
        """
        NumPy 타입과 같은 직렬화 불가능한 데이터를 표준 Python 타입으로 변환
        
        Parameters:
        - data: 변환할 데이터
        
        Returns:
        - 변환된 데이터
        """
        if isinstance(data, list):
            return [self._convert_to_serializable(item) for item in data]
        elif isinstance(data, dict):
            return {key: self._convert_to_serializable(value) for key, value in data.items()}
        elif isinstance(data, (np.int64, np.int32, np.int16, np.int8)):
            return int(data)
        elif isinstance(data, (np.float64, np.float32, np.float16)):
            return float(data)
        elif isinstance(data, np.bool_):
            return bool(data)
        elif isinstance(data, np.ndarray):
            return self._convert_to_serializable(data.tolist())
        else:
            return data
    
    def generate_dashboard(self, port=8050, open_browser=True):
        """
        대시보드 생성 및 실행
        
        Parameters:
        - port: 대시보드 실행 포트
        - open_browser: 브라우저 자동 실행 여부
        
        Returns:
        - 생성된 대시보드 URL
        """
        print("대시보드 생성 중...")
        
        try:
            # 템플릿 변수 준비
            template_vars = {
                'title': '엔트리 셀러 인사이트 대시보드',
                'subtitle': f'분석 기간: {self.insights.get("start_date", "알 수 없음")} ~ {self.insights.get("end_date", "알 수 없음")}'
            }
            
            # 인사이트 텍스트 생성
            template_vars['product_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'product')
            template_vars['color_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'color')
            template_vars['price_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'price')
            template_vars['channel_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'channel')
            template_vars['size_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'size')
            template_vars['material_design_insight'] = InsightsFormatter.generate_insight_text(self.summary, 'material_design')
            
            # 차트 데이터 형식화 (디버깅 추가)
            try:
                product_data = InsightsFormatter.format_table_data(self.insights, 'keywords')
                print(f"product_data 추출: {len(product_data)} 항목")
            except Exception as e:
                print(f"product_data 추출 중 오류: {e}")
                product_data = [{'name': '데이터 로드 오류', 'value': 0}]
            
            try:
                color_data = InsightsFormatter.format_table_data(self.insights, 'colors')
                print(f"color_data 추출: {len(color_data)} 항목")
            except Exception as e:
                print(f"color_data 추출 중 오류: {e}")
                color_data = [{'name': '데이터 로드 오류', 'value': 1}]
            
            try:
                price_data = InsightsFormatter.format_table_data(self.insights, 'prices')
                print(f"price_data 추출: {len(price_data)} 항목")
            except Exception as e:
                print(f"price_data 추출 중 오류: {e}")
                price_data = [{'name': '데이터 로드 오류', 'value': 0, 'percent': 0}]
            
            try:
                channel_data = InsightsFormatter.format_table_data(self.insights, 'channels')
                print(f"channel_data 추출: {len(channel_data)} 항목")
            except Exception as e:
                print(f"channel_data 추출 중 오류: {e}")
                channel_data = [{'name': '데이터 로드 오류', 'value': 0}]
            
            try:
                size_data = InsightsFormatter.format_table_data(self.insights, 'sizes')
                print(f"size_data 추출: {len(size_data)} 항목")
            except Exception as e:
                print(f"size_data 추출 중 오류: {e}")
                size_data = [{'name': '데이터 로드 오류', 'value': 1}]
            
            try:
                # 소재와 디자인 데이터 합치기
                material_data = InsightsFormatter.format_table_data(self.insights, 'materials')
                design_data = InsightsFormatter.format_table_data(self.insights, 'designs')
                material_design_data = material_data[:3] + design_data[:3]
                print(f"material_design_data 추출: {len(material_design_data)} 항목")
            except Exception as e:
                print(f"material_design_data 추출 중 오류: {e}")
                material_design_data = [{'name': '데이터 로드 오류', 'value': 0}]
            
            try:
                bestseller_data = InsightsFormatter.format_table_data(self.insights, 'bestsellers')
                print(f"bestseller_data 추출: {len(bestseller_data)} 항목")
            except Exception as e:
                print(f"bestseller_data 추출 중 오류: {e}")
                bestseller_data = [{'name': '데이터 로드 오류', 'value': 0}]
            
            # 빈 데이터 필터링 및 기본값 설정
            template_vars['product_data'] = product_data if product_data else [{'name': '데이터 없음', 'value': 0}]
            template_vars['color_data'] = color_data if color_data else [{'name': '데이터 없음', 'value': 1}]
            template_vars['price_data'] = price_data if price_data else [{'name': '데이터 없음', 'value': 0, 'percent': 0}]
            template_vars['channel_data'] = channel_data if channel_data else [{'name': '데이터 없음', 'value': 0}]
            template_vars['size_data'] = size_data if size_data else [{'name': '데이터 없음', 'value': 1}]
            template_vars['material_design_data'] = material_design_data if material_design_data else [{'name': '데이터 없음', 'value': 0}]
            template_vars['bestseller_data'] = bestseller_data if bestseller_data else [{'name': '데이터 없음', 'value': 0}]
            
            # 모든 데이터를 직렬화 가능한 형식으로 변환
            for key in template_vars:
                if key in ['product_data', 'color_data', 'price_data', 'channel_data', 
                        'size_data', 'material_design_data', 'bestseller_data']:
                    template_vars[key] = self._convert_to_serializable(template_vars[key])
            
            # 실행 가이드 생성
            guide = InsightsFormatter.get_execution_guide(self.summary)
            
            # 상품 추천
            template_vars['product_recommendations'] = []
            if guide and 'recommended_products' in guide:
                for i, product in enumerate(guide['recommended_products'][:3]):
                    template_vars['product_recommendations'].append({
                        'name': f"{i+1}. {product}" if isinstance(product, str) else f"{i+1}. 추천 상품",
                        'description': "인기 키워드 및 색상 조합"
                    })
            if not template_vars['product_recommendations']:
                template_vars['product_recommendations'] = [{'name': '추천 상품 데이터 없음', 'description': ''}]
            
            # 채널 & 가격 전략 추천
            template_vars['channel_recommendations'] = []
            if guide and 'channels' in guide and len(guide['channels']) > 0:
                for i, channel in enumerate(guide['channels'][:3]):
                    price_text = f" {guide['main_price_range']}에 집중" if 'main_price_range' in guide else ""
                    template_vars['channel_recommendations'].append({
                        'name': f"{channel} 채널",
                        'description': f"진입 중점 채널{price_text}"
                    })
            if not template_vars['channel_recommendations']:
                template_vars['channel_recommendations'] = [{'name': '채널 전략 데이터 없음', 'description': ''}]
            
            # 키워드 추천
            template_vars['keyword_recommendations'] = []
            if guide:
                if 'product_keywords' in guide and len(guide['product_keywords']) > 0:
                    template_vars['keyword_recommendations'].append({
                        'name': '상품 키워드',
                        'description': ', '.join(guide['product_keywords'][:3])
                    })
                if 'color_keywords' in guide and len(guide['color_keywords']) > 0:
                    template_vars['keyword_recommendations'].append({
                        'name': '색상',
                        'description': ', '.join(guide['color_keywords'][:3])
                    })
                if 'material_keywords' in guide and len(guide['material_keywords']) > 0:
                    template_vars['keyword_recommendations'].append({
                        'name': '소재',
                        'description': ', '.join(guide['material_keywords'][:3])
                    })
            if not template_vars['keyword_recommendations']:
                template_vars['keyword_recommendations'] = [{'name': '키워드 데이터 없음', 'description': ''}]
            
            # HTML 파일로 저장
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('dashboard_template.html')
            output = template.render(**template_vars)
            
            dashboard_file = self.output_folder / f"dashboard_{self.timestamp}.html"
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                f.write(output)
            
            print(f"HTML 대시보드가 생성되었습니다: {dashboard_file}")
            
            # 브라우저에서 열기
            if open_browser:
                webbrowser.open(f"file://{dashboard_file.resolve()}")
            
            return str(dashboard_file)
            
        except Exception as e:
            print(f"대시보드 생성 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None