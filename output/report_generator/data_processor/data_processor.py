# output/report_generator/data_processor/data_processor.py
"""
리포트용 데이터 처리 모듈 (간소화 버전)
"""
from datetime import datetime

from output.report_generator.data_processor.strategy_processor import StrategyProcessor
from output.report_generator.data_processor.auto_keyword_processor import AutoKeywordProcessor

class ReportDataProcessor:
    """리포트 데이터 통합 처리 클래스"""
    
    def __init__(self, insights, formatter):
        """
        데이터 처리기 초기화
        
        Parameters:
        - insights: 분석 결과 딕셔너리
        - formatter: InsightsFormatter 인스턴스
        """
        self.insights = insights
        self.formatter = formatter
        
        # 전략/자동 키워드 등 세부 프로세서
        self.strategy_processor = StrategyProcessor(formatter)
        self.auto_keyword_processor = AutoKeywordProcessor()
    
    def prepare_template_variables(self, now, summary):
        """
        템플릿 변수 준비 (간소화 버전)
        
        Parameters:
        - now: 현재 시각 (datetime)
        - summary: BaseGenerator에서 추출한 요약 정보
        
        Returns:
        - 템플릿에 전달할 변수 딕셔너리
        """
        template_vars = {
            'title': '엔트리 셀러 인사이트 리포트 (간소화)',
            'timestamp': now.strftime('%Y-%m-%d %H:%M'),
            'period': f"{self.insights.get('start_date', '알 수 없음')} ~ {self.insights.get('end_date', '알 수 없음')}",
            'total_orders': len(self.insights.get('df', [])) if 'df' in self.insights else summary.get('total_orders', 0),
            'current_year': datetime.now().year
        }

        # 1) 요약 정보 (간단 문장)
        template_vars.update(self._prepare_summary_variables(summary))

        # 2) 자동 키워드
        template_vars.update(self.auto_keyword_processor.prepare_auto_keywords_variables(self.insights))

        # 3) 전략
        template_vars.update(self.strategy_processor.prepare_strategy_variables(self.insights, summary))
        
        return template_vars
    
    def _prepare_summary_variables(self, summary):
        """
        요약 정보 변수 준비 - 간단 요약 형태로만.
        """
        # 예시로 핵심 인사이트 문장 3개만 담는다.
        summary_points = []
        
        # 상품군 인사이트
        if 'top_keywords' in summary and summary['top_keywords']:
            first_kw = summary['top_keywords'][0]
            summary_points.append(f"가장 많이 팔린 상품 유형은 '{first_kw['name']}'이며 총 {first_kw['count']}건 판매되었습니다.")
        else:
            summary_points.append("상품군 데이터를 확인할 수 없습니다.")
        
        # 채널 인사이트
        if 'top3_channels' in summary and summary['top3_channels']:
            ch = summary['top3_channels'][0]
            summary_points.append(f"주요 판매 채널은 '{ch}'가 가장 큰 비중을 차지합니다.")
        else:
            summary_points.append("판매 채널 데이터가 부족합니다.")
        
        # 가격대 인사이트
        if 'main_price_range' in summary and 'main_price_percent' in summary:
            summary_points.append(f"{summary['main_price_range']} 가격대가 전체 중 {summary['main_price_percent']:.1f}%로 가장 많이 판매되었습니다.")
        else:
            summary_points.append("가격대 분석 데이터가 충분하지 않습니다.")
        
        # 색상 인사이트 (간단 예시)
        if 'top_colors' in summary and summary['top_colors']:
            summary_points.append(f"가장 인기 있는 색상은 '{summary['top_colors'][0]['name']}'입니다.")
        
        # 반환
        return {
            'summary_insights': summary_points
        }
