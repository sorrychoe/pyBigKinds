import pandas as pd
from sklearn.decomposition import NMF, PCA, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

from .base import (
    counter_to_dataframe,
    duplication_remover,
    keyword_list,
    keyword_parser,
    word_counter,
)


def day_range(df):
    """날짜 범위 파악"""
    print("first day: ", df["일자"].min(), "\n", "last day: ", df["일자"].max())


def press_counter(df):
    """언론사 별 보도 빈도"""
    freq = df["언론사"].value_counts()
    brod_df = pd.DataFrame(freq).reset_index()
    brod_df.rename(columns={"index": "언론사", "언론사": "기사"}, inplace=True)
    return brod_df


def keyword_dataframe(df):
    """키워드 단어 빈도"""
    lis = keyword_list(df)
    keywords = keyword_parser(lis)
    counter = word_counter(keywords)
    df = counter_to_dataframe(counter)
    return df


def keyword_dataframe_no_duplicated(df):
    """키워드 중복 제거 단어 빈도"""
    lis = keyword_list(df)
    keywords = keyword_parser(lis)
    keywords_set = duplication_remover(keywords)
    counter = word_counter(keywords_set)
    df = counter_to_dataframe(counter)
    return df


def tfidf(df, press: str):
    """키워드 상대 빈도"""
    if press:
        df = df[press]
    lis = keyword_list(df)

    tfidfv = TfidfVectorizer()
    tdm = tfidfv.fit_transform(lis)

    word_count = (
        pd.DataFrame(
            {
                "단어": tfidfv.get_feature_names_out(),
                "빈도": tdm.sum(axis=0).flat,
            },
        )
        .sort_values("빈도", ascending=False)
        .reset_index(drop=True)
    )
    return word_count


def tfidf_vector(df):
    """tfidf vector"""
    lis = keyword_list(df)
    pipeline = Pipeline(
        [
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
        ],
    )
    vec = pipeline.fit_transform(lis).toarray()
    return vec


def normalize_vector(vec):
    """normalize vector"""
    vec_nor = Normalizer().fit_transform(vec)
    return vec_nor


def pca(vec, Random_State=123):
    """PCA"""

    pca_df = PCA(n_components=2, random_state=Random_State, copy=False).fit_transform(
        vec,
    )
    pca_df = pd.DataFrame(pca_df, columns=["component 0", "component 1"])

    return pca_df


def nmf(vec, Random_State=123):
    """NMF"""

    nmf_df = NMF(
        n_components=2, random_state=Random_State, init="random",
    ).fit_transform(vec)
    nmf_df = pd.DataFrame(nmf_df, columns=["component 0", "component 1"])

    return nmf_df


def t_sne(vec, learn_Rate=100):
    """t-sne"""

    tsne = TSNE(n_components=2, learning_rate=learn_Rate).fit_transform(vec)
    tsne_df = pd.DataFrame(tsne, columns=["component 0", "component 1"])

    return tsne_df


def lsa(vec):
    """LSA"""

    svd = TruncatedSVD(n_components=2).fit_transform(vec)
    svd_df = pd.DataFrame(data=svd, columns=["component 0", "component 1"])

    return svd_df
