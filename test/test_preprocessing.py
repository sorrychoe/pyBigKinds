import pytest
import pandas as pd
import numpy as np
from pyBigKinds import *

@pytest.fixture(scope="module")
def dataframe():
    df = pd.read_excel("test/test.xlsx")
    return df


def test_press_counter(dataframe):
    """언론사 별 보도 빈도"""
    counter = press_counter(dataframe)
    assert counter.columns[0] == '언론사'
    assert counter.columns[1] == '기사'
    assert counter['기사'].max() == counter['기사'][0]


def test_keyword_dataframe(dataframe):
    """키워드 단어 빈도"""
    data = keyword_dataframe(dataframe)
    assert data.columns[0] == '단어'
    assert data.columns[1] == '빈도'
    assert data['빈도'].max() == data['빈도'][0]


def test_keyword_dataframe_no_duplicated(dataframe):
    """키워드 중복 제거 단어 빈도"""
    data = keyword_dataframe_no_duplicated(dataframe)
    assert data.columns[0] == '단어'
    assert data.columns[1] == '빈도'
    assert data['빈도'].max() == data['빈도'][0]


def test_tfidf(dataframe):
    """키워드 상대 빈도"""
    df = tfidf(dataframe)
    assert df.columns[0] == '단어'
    assert df.columns[1] == '빈도'
    assert df['빈도'].max() == df['빈도'][0]


def test_tfidf_vector(dataframe):
    """tfidf vector"""
    vector = tfidf_vector(dataframe)
    assert type(vector) == np.ndarray
    assert vector.shape == (31,2160)



def test_normalize_vector(dataframe):
    """normalize vector"""
    vector = tfidf_vector(dataframe)
    normal = normalize_vector(vector)
    assert normal.shape == vector.shape


def test_pca(dataframe):
    vector = tfidf_vector(dataframe)
    pca_df = pca(vector)

    assert pca_df.columns[0] == 'component 0'
    assert pca_df.columns[1] == 'component 1'
    assert pca_df.shape == (31,2)


def test_nmf(dataframe):
    """NMF"""

    vector = tfidf_vector(dataframe)
    nmf_df = nmf(vector)

    assert nmf_df.columns[0] == 'component 0'
    assert nmf_df.columns[1] == 'component 1'
    assert nmf_df.shape == (31,2)


def test_t_sne(dataframe):
    """t-sne"""

    vector = tfidf_vector(dataframe)
    tsne_df = t_sne(vector, 100)

    assert tsne_df.columns[0] == 'component 0'
    assert tsne_df.columns[1] == 'component 1'
    assert tsne_df.shape == (31,2)


def test_lsa(dataframe):
    """LSA"""
    vector = tfidf_vector(dataframe)
    lsa_df = lsa(vector)

    assert lsa_df.columns[0] == 'component 0'
    assert lsa_df.columns[1] == 'component 1'
    assert lsa_df.shape == (31,2)