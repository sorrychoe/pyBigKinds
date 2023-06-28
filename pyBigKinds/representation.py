# pylint: disable=E1101

import numpy as np
import pandas as pd
import tomotopy as tp
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from sklearn.cluster import DBSCAN, KMeans, MeanShift, estimate_bandwidth
from sklearn.decomposition import NMF, PCA, TruncatedSVD
from sklearn.manifold import TSNE

from .base import keyword_list, keyword_parser


def day_range(df):
    """날짜 범위 파악"""
    if isinstance(df, pd.DataFrame):
        print("first day: ", df["일자"].min(), "\n", "last day: ", df["일자"].max())
    else:
        raise TypeError("input type is to be have to DataFrame")


def press_counter(df):
    """언론사 별 보도 빈도"""
    if isinstance(df, pd.DataFrame):
        freq = df["언론사"].value_counts()
        brod_df = pd.DataFrame(freq).reset_index()
        brod_df.rename(columns={"count": "기사"}, inplace=True)
        return brod_df
    else:
        raise TypeError("input type is to be have to DataFrame")


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


def meanshift(vec, qt=0.25):
    """Mean Shift"""
    if isinstance(vec, np.ndarray):
        best_bandwidth = estimate_bandwidth(vec, quantile=qt)
        print(f'{qt}기준 최적 bandwidth 값:', round(best_bandwidth, 2))

        ms_model = MeanShift(bandwidth=best_bandwidth)
        print('cluster 갯수:', np.unique(ms_model.fit_predict(vec)))
        return ms_model.fit_predict(vec)
    else:
        raise TypeError("input type is to be have to ndarray")


def lda(dataframe, k=10, train=100, fit=10):
    """topic modeling"""
    if isinstance(dataframe, pd.DataFrame):
        lis = keyword_parser(keyword_list(dataframe))
        model = tp.LDAModel(k=k)

        for words in lis:
            model.add_doc(words)

        for i in range(0, train, fit):
            model.train(i)

        return model
    else:
        raise TypeError("input type is to be have to DataFrame")


def association(dataframe, min_support=0.5, use_colnames=True, min_threshold=0.1, metric="confidence"):
    """apriopri"""
    words = keyword_parser(keyword_list(dataframe))
    te = TransactionEncoder()
    te_data = te.fit(words).transform(words, sparse=True)
    te_df = pd.DataFrame.sparse.from_spmatrix(te_data, columns=te.columns_)

    result = apriori(te_df, min_support=min_support, use_colnames=use_colnames)

    return association_rules(result, metric=metric, min_threshold=min_threshold)
