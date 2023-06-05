import pandas as pd
from pyBigKinds import *

import pytest

@pytest.fixture(scope="module")
def vector():
    df = pd.read_excel("test/test.xlsx")
    vector = tfidf_vector(df)
    return vector

def test_keywords_wordcloud(vector):
    """언론사 별 키워드 워드클라우드 생성"""
    with pytest.raises(TypeError):
        keywords_wordcloud(vector, "press")

def test_top_words(vector):
    """언론사 별 사용 단어 빈도 상위 25개"""
    with pytest.raises(TypeError):
        top_words(vector, "press")


def test_scatterplot(vector):
    """scatter plot for dimension reduction"""
    with pytest.raises(TypeError):
        scatterplot(vector, "label")
