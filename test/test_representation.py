from pyBigKinds import *

import numpy as np
import pandas as pd

import pytest

@pytest.fixture(scope="module")
def vector():
    df = pd.read_excel("test/test.xlsx")
    vector = tfidf_vector(df)
    return vector

@pytest.fixture(scope="module")
def dataframe():
    df = pd.read_excel("test/test.xlsx")
    return df

def test_press_counter(dataframe):
    counter = press_counter(dataframe)
    assert counter.columns[0] == '언론사'
    assert counter.columns[1] == '기사'
    assert counter['기사'].max() == counter['기사'][0]

def test_pca(vector):
    pca_df = pca(vector)

    assert pca_df.columns[0] == 'component 0'
    assert pca_df.columns[1] == 'component 1'
    assert pca_df.shape == (31,2)


def test_nmf(vector):
    nmf_df = nmf(vector)

    assert nmf_df.columns[0] == 'component 0'
    assert nmf_df.columns[1] == 'component 1'
    assert nmf_df.shape == (31,2)


def test_t_sne(vector):
    tsne_df = t_sne(vector, 100)

    assert tsne_df.columns[0] == 'component 0'
    assert tsne_df.columns[1] == 'component 1'
    assert tsne_df.shape == (31,2)


def test_lsa(vector):
    lsa_df = lsa(vector)

    assert lsa_df.columns[0] == 'component 0'
    assert lsa_df.columns[1] == 'component 1'
    assert lsa_df.shape == (31,2)


def test_kmeans(vector):
    cluster = kmeans(vector, 3, random_state=1000)
    assert type(cluster) == np.ndarray
    assert sum(np.unique(cluster)) == 3


def test_dbscan(vector):
    cluster = dbscan(vector, 0.1, 1)
    assert type(cluster) == np.ndarray


def test_lda(dataframe):
    topics = lda(dataframe)
    assert type(topics.vocab_df) == np.ndarray
    assert topics.k == 10


def test_association(dataframe):
    apriopri = association(dataframe)
    assert type(apriopri) == pd.DataFrame
    assert apriopri.shape == (8, 10)
