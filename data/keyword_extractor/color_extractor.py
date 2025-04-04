# data/keyword_extractor/color_extractor.py
"""
색상 그룹 추출 로직
"""
import re
import pandas as pd

class ColorExtractor:
    """색상 데이터 클러스터링/그룹 추출"""

    @staticmethod
    def extract_color_groups(option_texts, color_patterns):
        """
        옵션 텍스트에서 색상 그룹 추출
        Parameters:
        - option_texts: 시리즈 또는 리스트(옵션 텍스트)
        - color_patterns: 정규식으로 사용할 색상 패턴(|로 연결한 문자열)
        Returns:
        - [(색상, 빈도), ...] 형태의 상위 색상 리스트
        """
        if len(option_texts) == 0:
            return []

        color_regex = re.compile(r'(' + color_patterns + r')', re.IGNORECASE)

        colors = []
        for text in option_texts:
            matches = color_regex.findall(text)
            colors.extend(matches)

        if not colors:
            return []

        color_counts = pd.Series(colors).value_counts()
        top_colors = color_counts.head(20)

        return [(color, count) for color, count in top_colors.items()]
