# output/__init__.py
"""
비플로우 분석 시스템의 결과물 생성 모듈 - 대시보드 전용
"""
from output.base_generator import BaseGenerator
from output.dashboard_generator import DashboardGenerator

__all__ = ['BaseGenerator', 'DashboardGenerator']