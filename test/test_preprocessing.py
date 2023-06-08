import pytest
import pandas as pd
import numpy as np
from pyBigKinds import *

@pytest.fixture(scope="module")
def dataframe():
    df = pd.read_excel("test/test.xlsx")
    return df


def test_keyword_dataframe(dataframe):
    data = keyword_dataframe(dataframe)
    assert data.columns[0] == '단어'
    assert data.columns[1] == '빈도'
    assert data['빈도'].max() == data['빈도'][0]


def test_keyword_dataframe_no_duplicated(dataframe):
    data = keyword_dataframe_no_duplicated(dataframe)
    assert data.columns[0] == '단어'
    assert data.columns[1] == '빈도'
    assert data['빈도'].max() == data['빈도'][0]


def test_tfidf(dataframe):
    df = tfidf(dataframe)
    assert df.columns[0] == '단어'
    assert df.columns[1] == '빈도'
    assert df['빈도'].max() == df['빈도'][0]


def test_tfidf_vector(dataframe):
    vector = tfidf_vector(dataframe)
    assert type(vector) == np.ndarray
    assert vector.shape == (31,2160)


def test_normalize_vector(dataframe):
    vector = tfidf_vector(dataframe)
    normal = normalize_vector(vector)
    assert normal.shape == vector.shape
