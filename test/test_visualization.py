import pandas as pd
from pyBigKinds import *

import pytest

@pytest.fixture(scope="module")
def vector():
    df = pd.read_excel("test/test.xlsx")
    vector = tfidf_vector(df)
    return vector

def test_keywords_wordcloud(vector):
    with pytest.raises(TypeError):
        keywords_wordcloud(vector, "press")

def test_top_words(vector):
    with pytest.raises(TypeError):
        top_words(vector, "press")


def test_scatterplot(vector):
    with pytest.raises(TypeError):
        scatterplot(vector, "label")
