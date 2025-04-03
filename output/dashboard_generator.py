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
from visualization.chart_generator import ChartGenerator
from output.base_generator import BaseGenerator
from utils.utils import convert_to_serializable, safe_process_data

class DashboardGenerator(BaseGenerator):
    """비플로우 분석 결과를 바탕으로 대시보드 생성"""
    
    def __init__(self, insights, formatter=None, output_folder='bflow_reports', config=None):
        """
        대시보드 생성기 초기화
        
        Parameters:
        - insights: BflowAnalyzer에서 생성한 분석 결과
        - formatter: InsightsFormatter 인스턴스 (None이면 자동 생성)
        - output_folder: 결과물 저장 폴더
        - config: 설정 객체 (None이면 기본 설정 사용)
        """
        # 부모 클래스 초기화
        super().__init__(insights, formatter, output_folder)
        
        # 설정 객체 설정
        if config is None:
            from config.config import Config
            self.config = Config()
        else:
            self.config = config
        
        # 템플릿 경로 설정
        self.template_folder = Path(self.config.template_folder)
        
        # 디버깅 정보 출력
        print(f"DashboardGenerator 초기화 - insights 타입: {type(insights)}")
        print(f"DashboardGenerator 초기화 - summary 타입: {type(self.summary)}")
    
    def generate_dashboard(self, port=None, open_browser=True):
        """
        대시보드 생성 및 실행
        
        Parameters:
        - port: 대시보드 실행 포트 (None이면 설정에서 가져옴)
        - open_browser: 브라우저 자동 실행 여부
        
        Returns:
        - 생성된 대시보드 URL
        """
        print("대시보드 생성 중...")
        
        try:
            # 포트 설정
            if port is None:
                port = self.config.dashboard_port
                
            # 템플릿 변수 준비
            template_vars = self._prepare_template_variables()
            
            # 모든 데이터를 직렬화 가능한 형식으로 변환
            for key in template_vars:
                if key in ['product_data', 'color_data', 'price_data', 'channel_data', 
                        'size_data', 'material_design_data', 'bestseller_data']:
                    template_vars[key] = convert_to_serializable(template_vars[key])
            
            # HTML 파일로 저장
            env = Environment(loader=FileSystemLoader(self.template_folder))
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
    
    def _prepare_template_variables(self):
        """템플릿 변수 준비"""
        # 기본 정보
        template_vars = {
            'title': '엔트리 셀러 인사이트 대시보드',
            'subtitle': f'분석 기간: {self.insights.get("start_date", "알 수 없음")} ~ {self.insights.get("end_date", "알 수 없음")}'
        }
        
        # 인사이트 텍스트 생성
        template_vars['product_insight'] = self.formatter.generate_insight_text('product')
        template_vars['color_insight'] = self.formatter.generate_insight_text('color')
        template_vars['price_insight'] = self.formatter.generate_insight_text('price')
        template_vars['channel_insight'] = self.formatter.generate_insight_text('channel')
        template_vars['size_insight'] = self.formatter.generate_insight_text('size')
        template_vars['material_design_insight'] = self.formatter.generate_insight_text('material_design')
        
        # 차트 데이터 형식화 - safe_process_data 유틸리티 함수 사용
        template_vars['product_data'] = safe_process_data(
            self.formatter.format_table_data, 'keywords',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="product_data 추출 중 오류"
        )
        
        template_vars['color_data'] = safe_process_data(
            self.formatter.format_table_data, 'colors',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="color_data 추출 중 오류"
        )
        
        template_vars['price_data'] = safe_process_data(
            self.formatter.format_table_data, 'prices',
            default_value=[{'name': '데이터 로드 오류', 'value': 0, 'percent': 0}],
            error_message="price_data 추출 중 오류"
        )
        
        template_vars['channel_data'] = safe_process_data(
            self.formatter.format_table_data, 'channels',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="channel_data 추출 중 오류"
        )
        
        template_vars['size_data'] = safe_process_data(
            self.formatter.format_table_data, 'sizes',
            default_value=[{'name': '데이터 로드 오류', 'value': 1}],
            error_message="size_data 추출 중 오류"
        )
        
        # 소재와 디자인 데이터 합치기
        try:
            material_data = self.formatter.format_table_data('materials')
            design_data = self.formatter.format_table_data('designs')
            material_design_data = material_data[:3] + design_data[:3]
            print(f"material_design_data 추출: {len(material_design_data)} 항목")
        except Exception as e:
            print(f"material_design_data 추출 중 오류: {e}")
            material_design_data = [{'name': '데이터 로드 오류', 'value': 0}]
        
        template_vars['material_design_data'] = material_design_data
        
        template_vars['bestseller_data'] = safe_process_data(
            self.formatter.format_table_data, 'bestsellers',
            default_value=[{'name': '데이터 로드 오류', 'value': 0}],
            error_message="bestseller_data 추출 중 오류"
        )
        
        # 빈 데이터 필터링 및 기본값 설정
        template_vars['product_data'] = template_vars['product_data'] if template_vars['product_data'] else [{'name': '데이터 없음', 'value': 0}]
        template_vars['color_data'] = template_vars['color_data'] if template_vars['color_data'] else [{'name': '데이터 없음', 'value': 1}]
        template_vars['price_data'] = template_vars['price_data'] if template_vars['price_data'] else [{'name': '데이터 없음', 'value': 0, 'percent': 0}]
        template_vars['channel_data'] = template_vars['channel_data'] if template_vars['channel_data'] else [{'name': '데이터 없음', 'value': 0}]
        template_vars['size_data'] = template_vars['size_data'] if template_vars['size_data'] else [{'name': '데이터 없음', 'value': 1}]
        template_vars['material_design_data'] = material_design_data if material_design_data else [{'name': '데이터 없음', 'value': 0}]
        template_vars['bestseller_data'] = template_vars['bestseller_data'] if template_vars['bestseller_data'] else [{'name': '데이터 없음', 'value': 0}]
        
        # 실행 가이드 생성
        guide = self.formatter.get_execution_guide()
        
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
        
        return template_vars