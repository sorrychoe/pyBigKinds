# pylint: disable=E0601,W0612

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import NMF, PCA, TruncatedSVD
from sklearn.manifold import TSNE


def pca(vec, Random_State=123):
    """PCA"""
    if isinstance(vec, np.ndarray):
        pca_df = PCA(n_components=2, random_state=Random_State, copy=False).fit_transform(
            vec,
        )
        pca_df = pd.DataFrame(pca_df, columns=["component 0", "component 1"])

        return pca_df
    else:
        raise TypeError("input type is to be have to ndarray")


def nmf(vec, Random_State=123):
    """NMF"""
    if isinstance(vec, np.ndarray):
        nmf_df = NMF(
            n_components=2, random_state=Random_State, init="random",
        ).fit_transform(vec)
        nmf_df = pd.DataFrame(nmf_df, columns=["component 0", "component 1"])

        return nmf_df
    else:
        raise TypeError("input type is to be have to ndarray")


def t_sne(vec, learn_Rate=100):
    """t-sne"""
    if isinstance(vec, np.ndarray):
        tsne = TSNE(n_components=2, learning_rate=learn_Rate).fit_transform(vec)
        tsne_df = pd.DataFrame(tsne, columns=["component 0", "component 1"])
    else:
        raise TypeError("input type is to be have to ndarray")

    return tsne_df


def lsa(vec):
    """LSA"""
    if isinstance(vec, np.ndarray):
        svd = TruncatedSVD(n_components=2).fit_transform(vec)
        svd_df = pd.DataFrame(data=svd, columns=["component 0", "component 1"])
    else:
        raise TypeError("input type is to be have to ndarray")

    return svd_df


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
