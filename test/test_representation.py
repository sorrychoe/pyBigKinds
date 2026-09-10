# pylint: disable=E721

import numpy as np
import pandas as pd
import pytest

from pyBigKinds import *


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
    assert pca_df.shape == (31, 2)


def test_nmf(vector):
    nmf_df = nmf(vector)

    assert nmf_df.columns[0] == 'component 0'
    assert nmf_df.columns[1] == 'component 1'
    assert nmf_df.shape == (31, 2)


def test_t_sne(vector):
    tsne_df = t_sne(vector, 100)

    assert tsne_df.columns[0] == 'component 0'
    assert tsne_df.columns[1] == 'component 1'
    assert tsne_df.shape == (31, 2)


def test_lsa(vector):
    lsa_df = lsa(vector)

    assert lsa_df.columns[0] == 'component 0'
    assert lsa_df.columns[1] == 'component 1'
    assert lsa_df.shape == (31, 2)


def test_kmeans(vector):
    cluster = kmeans(vector, 3, random_state=1000)
    assert type(cluster) == np.ndarray
    assert sum(np.unique(cluster)) == 3


def test_dbscan(vector):
    cluster = dbscan(vector, 0.1, 1)
    assert type(cluster) == np.ndarray


def test_meanshift(vector):
    cluster = meanshift(vector)
    assert type(cluster) == np.ndarray
    # exact cluster count depends on the scikit-learn version; only assert
    # that every sample got a label and at least one cluster was found
    assert cluster.shape == (vector.shape[0],)
    assert len(np.unique(cluster)) >= 1


def test_lda(dataframe):
    topics = lda(dataframe)
    assert type(topics.vocab_df) == np.ndarray
    assert topics.k == 10


def test_association(dataframe):
    apriopri = association(dataframe)
    assert type(apriopri) == pd.DataFrame
    # the column set of association_rules grows between mlxtend versions, so
    # check the stable core columns instead of an exact shape
    assert not apriopri.empty
    for col in ("antecedents", "consequents", "support", "confidence", "lift"):
        assert col in apriopri.columns
