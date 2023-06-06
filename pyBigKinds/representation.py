# pylint: disable=E0601,W0612

import numpy as np
from sklearn.cluster import DBSCAN, KMeans


def kmeans(vec, k, random_state=123):
    """K-Means"""
    if isinstance(vec, np.ndarray):
        kmeans_model = KMeans(n_clusters=k, max_iter=1000, random_state=random_state)
        return kmeans_model.fit_predict(vec)
    else:
        raise TypeError("input type is to be have to ndarray")


def dbscan(vec, eps, min_samples, metric="euclidean"):
    """DBSCAN"""
    if isinstance(vec, np.ndarray):
        dbscan_model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
        return dbscan_model.fit_predict(vec)
    else:
        raise TypeError("input type is to be have to ndarray")
