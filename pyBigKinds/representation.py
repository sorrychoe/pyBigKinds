# pylint: disable=E0601,W0612

from sklearn.cluster import DBSCAN, KMeans


def kmeans(vec, k, random_state=None):
    """K-Means"""
    kmeans_model = KMeans(n_clusters=k, max_iter=1000, random_state=random_state)
    return kmeans_model.fit_predict(vec)


def dbscan(vec, eps, min_samples, metric="euclidean"):
    """DBSCAN"""
    dbscan_model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    return dbscan_model.fit_predict(vec)
