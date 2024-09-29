# pylint: disable=C0301

import pandas as pd


def header_remover(df):
    """
    Removes any text enclosed in square brackets ([]) from the 'title' column of a DataFrame or list.

    Parameters:
    df (pandas.DataFrame or list): The input DataFrame or list containing a column or text data where headers (enclosed in square brackets) need to be removed.

    Returns:
    pandas.Series or list: A pandas Series or list with the cleaned text where square bracketed sections are removed.

    Raises:
    TypeError: If the input is not a pandas DataFrame or list.
    """
    if isinstance(df, pd.DataFrame):
        ans = df["제목"].str.replace(r"\[[^)]*\]", "", regex=True)
    elif isinstance(df, list):
        ans = df.str.replace(r"\[[^)]*\]", "", regex=True)
    else:
        raise TypeError("input value is to be have to list or DataFrame")
    return ans


def keyword_list(df):
    """
    Converts the '키워드' column of a DataFrame to a list or returns a list as-is if the input is already a list.

    Parameters:
    df (pandas.DataFrame or list): The input DataFrame containing the '키워드' column or a list to be converted to a list format.

    Returns:
    list: A list of keywords from the '키워드' column of the DataFrame, or a list itself if the input is a list.

    Raises:
    TypeError: If the input is not a pandas DataFrame or list.
    """
    if isinstance(df, pd.DataFrame):
        return df["키워드"].values.tolist()
    elif isinstance(df, list):
        return df.values.tolist()
    else:
        raise TypeError("input value is to be have to list or DataFrame")


def keyword_parser(text_list):
    """
    Parses and splits a list of keywords into individual words by separating them based on commas.

    Parameters:
    text_list (list): A list of strings where each string contains keywords separated by commas.

    Returns:
    list of lists: A list where each element is a sublist of keywords split from the original list of strings.

    Raises:
    TypeError: If the input is not a list.
    ValueError: If any element in the list is not a valid string format.
    """
    if isinstance(text_list, list):
        news_key = []
        for word in text_list:
            if isinstance(word, str):
                word = word.split(",")
                news_key.append(word)
            else:
                raise ValueError("input list is not valid format")
        return news_key
    else:
        raise TypeError("input type is to be have to list")


def duplication_remover(news_key):
    """
    Removes duplicate keywords from a list of lists.

    Parameters:
    news_key (list): A list where each element is a list of keywords.

    Returns:
    list of lists: A list where duplicate keywords within each sublist have been removed.

    Raises:
    TypeError: If the input is not a list of lists.
    ValueError: If any element in the list is not a valid sublist.
    """
    if isinstance(news_key, list):
        news_value = []
        for j in news_key:
            if isinstance(j, list):
                j = list(set(j))
                news_value.append(j)
            else:
                raise ValueError("input list is not valid format")
        return news_value
    else:
        raise TypeError("input type is to be have to list")


def word_counter(news_value):
    """
    Counts the occurrence of each keyword from a list of lists of keywords.

    Parameters:
    news_value (list): A list where each element is a list of keywords.

    Returns:
    dict: A dictionary where each key is a keyword and each value is the frequency of that keyword.

    Raises:
    TypeError: If the input is not a list of lists.
    """
    if isinstance(news_value, list):
        key_words = {}
        for k in range(len(news_value)):
            for i in news_value[k]:
                if i not in key_words:
                    key_words[i] = 1
                elif i in key_words:
                    key_words[i] += 1
        return key_words
    else:
        raise TypeError("input type is to be have to list")


def counter_to_dataframe(key_words):
    """
    Converts a dictionary of keyword counts into a sorted pandas DataFrame.

    Parameters:
    key_words (dict): A dictionary where each key is a keyword and each value is the frequency of that keyword.

    Returns:
    pandas.DataFrame: A DataFrame with two columns: '단어' (keyword) and '빈도' (frequency), sorted by frequency in descending order.

    Raises:
    TypeError: If the input is not a dictionary.
    """
    if isinstance(key_words, dict):
        word_df = pd.DataFrame(key_words.items())
        word_df.columns = ["단어", "빈도"]
        word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(
            drop=True,
        )
        return word_df
    else:
        raise TypeError("input type is to be have to dict")
