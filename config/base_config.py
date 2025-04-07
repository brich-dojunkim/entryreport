# config/base_config.py
"""
기본 설정 클래스를 제공하는 모듈
"""
import os

class BaseConfig:
    """
    환경 변수나 기본값에서 설정을 로드하는 기본 클래스
    """
    
    def __init__(self):
        """
        설정 초기화
        """
        pass
    
    def get_env_value(self, var_name, default_value):
        """
        환경 변수에서 값을 가져오거나 기본값 반환
        
        Parameters:
        - var_name: 환경 변수 이름
        - default_value: 기본값
        
        Returns:
        - 환경 변수 값 또는 기본값
        """
        return os.environ.get(var_name, default_value)
    
    def get_env_int(self, var_name, default_value):
        """
        환경 변수에서 정수 값을 가져오거나 기본값 반환
        
        Parameters:
        - var_name: 환경 변수 이름
        - default_value: 기본값
        
        Returns:
        - 환경 변수의 정수 값 또는 기본값
        """
        try:
            return int(os.environ.get(var_name, default_value))
        except (ValueError, TypeError):
            return default_value
    
    def get_env_list(self, var_name, default_list=None):
        """
        환경 변수에서 쉼표로 구분된 목록을 가져오거나 기본 목록 반환
        
        Parameters:
        - var_name: 환경 변수 이름
        - default_list: 기본 목록
        
        Returns:
        - 환경 변수의 목록 또는 기본 목록
        """
        if default_list is None:
            default_list = []
            
        env_value = os.environ.get(var_name, '')
        if env_value:
            return default_list + env_value.split(',')
        return default_list