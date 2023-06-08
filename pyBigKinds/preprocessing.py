import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
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
    if isinstance(df, pd.DataFrame):
        print("first day: ", df["일자"].min(), "\n", "last day: ", df["일자"].max())
    else:
        raise TypeError("input type is to be have to DataFrame")


def press_counter(df):
    """언론사 별 보도 빈도"""
    if isinstance(df, pd.DataFrame):
        freq = df["언론사"].value_counts()
        brod_df = pd.DataFrame(freq).reset_index()
        brod_df.rename(columns={"index": "언론사", "언론사": "기사"}, inplace=True)
        return brod_df
    else:
        raise TypeError("input type is to be have to DataFrame")


def keyword_dataframe(df):
    """키워드 단어 빈도"""
    if isinstance(df, pd.DataFrame):
        lis = keyword_list(df)
        keywords = keyword_parser(lis)
        counter = word_counter(keywords)
        df = counter_to_dataframe(counter)
        return df
    else:
        raise TypeError("input type is to be have to DataFrame")


def keyword_dataframe_no_duplicated(df):
    """키워드 중복 제거 단어 빈도"""
    if isinstance(df, pd.DataFrame):
        lis = keyword_list(df)
        keywords = keyword_parser(lis)
        keywords_set = duplication_remover(keywords)
        counter = word_counter(keywords_set)
        df = counter_to_dataframe(counter)
        return df
    else:
        raise TypeError("input type is to be have to DataFrame")


def tfidf(df, *press):
    """키워드 상대 빈도"""
    if isinstance(df, pd.DataFrame):
        if isinstance(press, str):
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
    else:
        raise TypeError("input type is to be have to DataFrame")


def tfidf_vector(df):
    """tfidf vector"""
    if isinstance(df, pd.DataFrame):
        lis = keyword_list(df)
        pipeline = Pipeline(
            [
                ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
            ],
        )
        vec = pipeline.fit_transform(lis).toarray()
        return vec
    else:
        raise TypeError("input type is to be have to DataFrame")


def normalize_vector(vec):
    """normalize vector"""
    if isinstance(vec, np.ndarray):
        vec_nor = Normalizer().fit_transform(vec)
        return vec_nor
    else:
        raise TypeError("input type is to be have to ndarray")
