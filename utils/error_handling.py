def safe_process_data(func, *args, default_value=None, error_message="데이터 처리 중 오류", **kwargs):
    """
    안전하게 함수를 실행하고 예외 처리
    
    Parameters:
    - func: 실행할 함수
    - args: 함수에 전달할 위치 인수
    - default_value: 오류 발생시 반환할 기본값
    - error_message: 오류 발생시 출력할 메시지
    - kwargs: 함수에 전달할 키워드 인수
    
    Returns:
    - 함수 실행 결과 또는 오류 발생시 기본값
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"{error_message}: {e}")
        import traceback
        traceback.print_exc()
        return default_value
