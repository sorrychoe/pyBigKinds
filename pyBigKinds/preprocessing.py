# pylint: disable=C0301

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


def keyword_dataframe(df):
    """
    Generates a DataFrame of keyword frequencies based on the '키워드' column in the input DataFrame.

    This function extracts keywords from the '키워드' column, parses them, and counts the occurrence of each keyword.
    The result is returned as a DataFrame with columns for the keyword and its frequency.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing a '키워드' column with keywords.

    Returns:
    pandas.DataFrame: A DataFrame with two columns - '단어' (keyword) and '빈도' (frequency), sorted by frequency in descending order.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
    if isinstance(df, pd.DataFrame):
        lis = keyword_list(df)
        keywords = keyword_parser(lis)
        counter = word_counter(keywords)
        df = counter_to_dataframe(counter)
        return df
    else:
        raise TypeError("input type is to be have to DataFrame")


def keyword_dataframe_no_duplicated(df):
    """
    Generates a DataFrame of keyword frequencies after removing duplicate keywords.

    This function extracts keywords from the '키워드' column, removes duplicate keywords within each list, and counts the occurrence of each unique keyword.
    The result is returned as a DataFrame with columns for the keyword and its frequency.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing a '키워드' column with keywords.

    Returns:
    pandas.DataFrame: A DataFrame with two columns - '단어' (keyword) and '빈도' (frequency), sorted by frequency in descending order.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
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
    """
    Calculates the Term Frequency-Inverse Document Frequency (TF-IDF) for keywords in the input DataFrame.

    This function takes an optional column name (press) to select a specific column for TF-IDF calculations. It uses the TfidfVectorizer to compute TF-IDF values for the keywords
    and returns a DataFrame of words with their corresponding TF-IDF scores.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing text data, typically in a '키워드' column.
    press (str, optional): A column name specifying which column to apply the TF-IDF transformation. Defaults to None.

    Returns:
    pandas.DataFrame: A DataFrame with two columns - '단어' (keyword) and '빈도' (TF-IDF score), sorted by score in descending order.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
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
    """
    Creates a TF-IDF vector representation of the keywords in the input DataFrame.

    This function uses a scikit-learn Pipeline that combines CountVectorizer and TfidfTransformer to generate a TF-IDF matrix (vectorized form) for the keywords in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing a '키워드' column with keywords.

    Returns:
    numpy.ndarray: A 2D array where each row corresponds to the TF-IDF vector for the keywords in each row of the DataFrame.

    Raises:
    TypeError: If the input is not a pandas DataFrame.
    """
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
    """
    Normalizes a TF-IDF vector or any other vector to unit length (L2 norm).

    This function uses the Normalizer from scikit-learn to scale each vector such that the Euclidean norm of each vector becomes 1.

    Parameters:
    vec (numpy.ndarray): A 2D array where each row is a vector to be normalized.

    Returns:
    numpy.ndarray: A 2D array with normalized vectors.

    Raises:
    TypeError: If the input is not a numpy ndarray.
    """
    if isinstance(vec, np.ndarray):
        vec_nor = Normalizer().fit_transform(vec)
        return vec_nor
    else:
        raise TypeError("input type is to be have to ndarray")
