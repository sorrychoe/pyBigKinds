from pyBigKinds import *

import numpy as np
import pandas as pd

import pytest

@pytest.fixture(scope="module")
def vector():
    df = pd.read_excel("test/test.xlsx")
    vector = tfidf_vector(df)
    return vector


def test_kmeans(vector):
    """K-Means"""
    cluster = kmeans(vector, 3, random_state=1000)
    assert type(cluster) == np.ndarray
    assert sum(np.unique(cluster)) == 3


def test_dbscan(vector):
    """DBSCAN"""
    cluster = dbscan(vector, 0.1, 1)
    assert type(cluster) == np.ndarray
