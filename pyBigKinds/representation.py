# pylint: disable=E1101, C0301

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
    """
    Prints the first and last date in the '일자' (date) column of a DataFrame.

    This function prints the minimum and maximum values from the '일자' column to display the range of dates in the dataset.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing a '일자' column with date values.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
    if isinstance(df, pd.DataFrame):
        print("first day: ", df["일자"].min(), "\n", "last day: ", df["일자"].max())
    else:
        raise TypeError("input type is to be have to DataFrame")


def press_counter(df):
    """
    Counts the number of news articles by press company in the '언론사' column.

    This function counts the occurrences of each press company in the '언론사' column, then returns a DataFrame
    showing the press companies and the number of articles.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing an '언론사' column with press company names.

    Returns:
    pandas.DataFrame: A DataFrame with two columns - '언론사' (press company) and '기사' (number of articles).

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
    if isinstance(df, pd.DataFrame):
        brod_df = (
            df["언론사"]
            .value_counts()
            .rename_axis("언론사")
            .reset_index(name="기사")
        )
        return brod_df
    else:
        raise TypeError("input type is to be have to DataFrame")


def pca(vec, random_state=123):
    """
    Performs Principal Component Analysis (PCA) on a vector to reduce its dimensions to 2 components.

    This function applies PCA to reduce the input vector to 2 dimensions, returning a DataFrame
    with the two principal components.

    Parameters:
    vec (numpy.ndarray): The input array to perform PCA on.
    random_state (int, optional): The random seed for reproducibility. Default is 123.

    Returns:
    pandas.DataFrame: A DataFrame containing two columns - 'component 0' and 'component 1', representing the two PCA components.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        pca_df = PCA(n_components=2, random_state=random_state).fit_transform(vec)
        pca_df = pd.DataFrame(pca_df, columns=["component 0", "component 1"])

        return pca_df
    else:
        raise TypeError("input type is to be have to ndarray")


def nmf(vec, random_state=123):
    """
    Performs Non-Negative Matrix Factorization (NMF) to reduce the dimensionality of a vector.

    This function applies NMF to reduce the input vector to 2 dimensions, returning a DataFrame
    with two components.

    Parameters:
    vec (numpy.ndarray): The input array to perform NMF on.
    random_state (int, optional): The random seed for reproducibility. Default is 123.

    Returns:
    pandas.DataFrame: A DataFrame containing two columns - 'component 0' and 'component 1', representing the two NMF components.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        nmf_df = NMF(
            n_components=2, random_state=random_state, init="random",
        ).fit_transform(vec)
        nmf_df = pd.DataFrame(nmf_df, columns=["component 0", "component 1"])

        return nmf_df
    else:
        raise TypeError("input type is to be have to ndarray")


def t_sne(vec, learning_rate=100):
    """
    Performs t-Distributed Stochastic Neighbor Embedding (t-SNE) to visualize high-dimensional data.

    This function applies t-SNE to reduce the input vector to 2 dimensions for visualization.

    Parameters:
    vec (numpy.ndarray): The input array to perform t-SNE on.
    learning_rate (int, optional): The learning rate for the t-SNE algorithm. Default is 100.

    Returns:
    pandas.DataFrame: A DataFrame containing two columns - 'component 0' and 'component 1', representing the two t-SNE components.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        tsne = TSNE(
            n_components=2, learning_rate=learning_rate, init="random",
        ).fit_transform(vec)
        tsne_df = pd.DataFrame(tsne, columns=["component 0", "component 1"])
    else:
        raise TypeError("input type is to be have to ndarray")

    return tsne_df


def lsa(vec):
    """
    Performs Latent Semantic Analysis (LSA) using Truncated SVD on a vector to reduce its dimensions.

    This function applies LSA (via TruncatedSVD) to reduce the input vector to 2 dimensions.

    Parameters:
    vec (numpy.ndarray): The input array to perform LSA on.

    Returns:
    pandas.DataFrame: A DataFrame containing two columns - 'component 0' and 'component 1', representing the two LSA components.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        svd = TruncatedSVD(n_components=2).fit_transform(vec)
        svd_df = pd.DataFrame(data=svd, columns=["component 0", "component 1"])
    else:
        raise TypeError("input type is to be have to ndarray")

    return svd_df


def kmeans(vec, k, random_state=123):
    """
    Applies K-Means clustering to a vector to group data into clusters.

    This function applies the K-Means algorithm to group the input data into 'k' clusters.

    Parameters:
    vec (numpy.ndarray): The input array to cluster.
    k (int): The number of clusters to form.
    random_state (int, optional): The random seed for reproducibility. Default is 123.

    Returns:
    numpy.ndarray: The cluster labels for each data point.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        kmeans_model = KMeans(n_clusters=k, max_iter=1000, random_state=random_state)
        return kmeans_model.fit_predict(vec)
    else:
        raise TypeError("input type is to be have to ndarray")


def dbscan(vec, eps, min_samples, metric="euclidean"):
    """
    Applies Density-Based Spatial Clustering of Applications with Noise (DBSCAN) to a vector.

    This function applies DBSCAN to group the input data into clusters based on density.

    Parameters:
    vec (numpy.ndarray): The input array to cluster.
    eps (float): The maximum distance between two samples for them to be considered as in the same neighborhood.
    min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point.
    metric (str, optional): The distance metric used. Default is 'euclidean'.

    Returns:
    numpy.ndarray: The cluster labels for each data point.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        dbscan_model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
        return dbscan_model.fit_predict(vec)
    else:
        raise TypeError("input type is to be have to ndarray")


def meanshift(vec, qt=0.25):
    """
    Applies Mean Shift clustering to a vector.

    This function applies Mean Shift clustering to group the input data into clusters.
    The bandwidth is automatically estimated based on the quantile value.

    Parameters:
    vec (numpy.ndarray): The input array to cluster.
    qt (float, optional): The quantile to use for estimating the bandwidth. Default is 0.25.

    Returns:
    numpy.ndarray: The cluster labels for each data point.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        best_bandwidth = estimate_bandwidth(vec, quantile=qt)
        print(f'{qt}기준 최적 bandwidth 값:', round(best_bandwidth, 2))

        ms_model = MeanShift(bandwidth=best_bandwidth)
        labels = ms_model.fit_predict(vec)
        print('cluster 갯수:', len(np.unique(labels)))
        return labels
    else:
        raise TypeError("input type is to be have to ndarray")


def lda(dataframe, k=10, train=100, fit=10):
    """
    Applies Latent Dirichlet Allocation (LDA) for topic modeling on a DataFrame.

    This function extracts keywords from a DataFrame, then applies LDA to find 'k' topics in the data.

    Parameters:
    dataframe (pandas.DataFrame): The input DataFrame containing text data.
    k (int, optional): The number of topics to find. Default is 10.
    train (int, optional): The number of training iterations. Default is 100.
    fit (int, optional): The number of iterations for each training step. Default is 10.

    Returns:
    tomotopy.LDAModel: The trained LDA model.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
    if isinstance(dataframe, pd.DataFrame):
        lis = keyword_parser(keyword_list(dataframe))
        model = tp.LDAModel(k=k)

        for words in lis:
            model.add_doc(words)

        for _ in range(0, train, fit):
            model.train(fit)

        return model
    else:
        raise TypeError("input type is to be have to DataFrame")


def association(dataframe, min_support=0.5, use_colnames=True, min_threshold=0.1, metric="confidence"):
    """
    Applies the Apriori algorithm to discover association rules from keywords in a DataFrame.

    This function extracts keywords, applies the Apriori algorithm to find frequent itemsets,
    and generates association rules based on the specified metric.

    Parameters:
    dataframe (pandas.DataFrame): The input DataFrame containing text data.
    min_support (float, optional): The minimum support for the Apriori algorithm. Default is 0.5.
    use_colnames (bool, optional): Whether to use column names in the resulting DataFrame. Default is True.
    min_threshold (float, optional): The minimum threshold for association rule generation. Default is 0.1.
    metric (str, optional): The metric to use for evaluating association rules. Default is 'confidence'.

    Returns:
    pandas.DataFrame: A DataFrame containing the association rules.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    ValueError: If no frequent itemsets meet ``min_support``.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("input type is to be have to DataFrame")

    words = keyword_parser(keyword_list(dataframe))
    te = TransactionEncoder()
    te_data = te.fit(words).transform(words, sparse=True)
    te_df = pd.DataFrame(
        {
            col: pd.arrays.SparseArray(te_data[:, i].toarray().ravel().astype(bool))
            for i, col in enumerate(te.columns_)
        },
    )

    result = apriori(te_df, min_support=min_support, use_colnames=use_colnames)
    if result.empty:
        raise ValueError(
            "No frequent itemsets found; try lowering min_support.",
        )

    return association_rules(result, metric=metric, min_threshold=min_threshold)
