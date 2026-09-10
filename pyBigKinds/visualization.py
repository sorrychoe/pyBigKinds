# pylint: disable=W0612, C0301
import logging
import platform

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import wordcloud

from .base import (
    counter_to_dataframe,
    duplication_remover,
    keyword_list,
    keyword_parser,
    word_counter,
)

logger = logging.getLogger(__name__)


def _resolve_korean_font():
    """
    Finds a Korean-capable font installed on the current operating system.

    Returns:
    tuple: (family_name, font_path). ``family_name`` is applied to matplotlib's
    ``font.family`` rcParam and ``font_path`` is passed to WordCloud. When no
    Korean font is available, matplotlib's default family is returned together
    with ``None`` (WordCloud then falls back to its bundled font, which cannot
    render Hangul) and a warning is logged.
    """
    system = platform.system()
    if system == "Windows":
        candidates = ["Malgun Gothic", "NanumGothic", "Gulim", "Batang"]
    elif system == "Darwin":
        candidates = ["AppleGothic", "Apple SD Gothic Neo", "NanumGothic"]
    else:  # Linux and every other platform
        candidates = ["NanumGothic", "NanumBarunGothic", "Noto Sans CJK KR", "UnDotum"]

    available = {font.name for font in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            try:
                path = fm.findfont(
                    fm.FontProperties(family=name), fallback_to_default=False,
                )
                return name, path
            except ValueError:
                continue

    logger.warning(
        "No Korean font found for '%s'. "
        "Hangul may not render correctly; install e.g. 'NanumGothic'.",
        system,
    )
    default_family = plt.rcParams["font.family"]
    return (default_family[0] if isinstance(default_family, list) else default_family), None


FONT_FAMILY, FONT_PATH = _resolve_korean_font()
plt.rcParams["font.family"] = FONT_FAMILY
plt.rcParams["axes.unicode_minus"] = False


def keywords_wordcloud(df, press):
    """
    Generates a WordCloud for keywords based on a specific press company in the DataFrame.

    This function filters the input DataFrame by the specified press company, extracts keywords,
    removes duplicates, counts keyword frequencies, and generates a WordCloud image from the frequencies.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing text data, typically with '언론사' and '키워드' columns.
    press (str): The name of the press company to filter the DataFrame by.

    Raises:
    TypeError: If the input is not a pandas DataFrame.

    Returns:
    None: Displays the WordCloud visualization.
    """
    if isinstance(df, pd.DataFrame):
        df_keywords = df[df["언론사"] == press]
        keywords = keyword_list(df_keywords)
        news_key = keyword_parser(keywords)
        news_key = duplication_remover(news_key)
        key = word_counter(news_key)
        news_key = counter_to_dataframe(key)
        wc = wordcloud.WordCloud(
            font_path=FONT_PATH,
            width=500,
            height=500,
            background_color="white",
        ).generate_from_frequencies(news_key.set_index("단어").to_dict()["빈도"])

        plt.imshow(wc)
        plt.axis("off")
        plt.show()
    else:
        raise TypeError("input type is to be have to DataFrame")


def top_words(df, press, top_n=25):
    """
    Displays a horizontal bar chart of the top N most frequently used words for a specific press company.

    This function filters the input DataFrame by the specified press company, extracts keywords, removes duplicates,
    and counts the frequency of each word. It then displays a bar chart showing the top N words by frequency.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing text data, typically with '언론사' and '키워드' columns.
    press (str): The name or partial name of the press company to filter the DataFrame by.
    top_n (int, optional): The number of top words to display. Default is 25.

    Raises:
    TypeError: If the input is not a pandas DataFrame.

    Returns:
    None: Displays a horizontal bar chart.
    """
    if isinstance(df, pd.DataFrame):
        df_keywords = df[df["언론사"].str.contains(press, regex=False, na=False)]
        keywords = keyword_list(df_keywords)
        news_key = keyword_parser(keywords)
        news_key = duplication_remover(news_key)
        key = word_counter(news_key)
        news_key = counter_to_dataframe(key)

        # counter_to_dataframe is sorted by frequency descending; reverse the
        # head so the longest bar sits at the top while labels stay aligned
        # with their own counts.
        data = news_key.head(top_n).iloc[::-1]
        plt.barh(data["단어"], data["빈도"])
        plt.tight_layout()
        plt.show()
    else:
        raise TypeError("input type is to be have to DataFrame")


def scatterplot(df, label):
    """
    Creates a scatter plot for visualizing dimension reduction results with group labels.

    This function plots the two components (e.g., from PCA, t-SNE, NMF) and colors the points based on the specified group labels.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing at least two columns, 'component 0' and 'component 1', representing reduced dimensions.
    label (str): The column name in the DataFrame containing group labels for coloring the scatter plot points.

    Raises:
    TypeError: If the input is not a pandas DataFrame.

    Returns:
    None: Displays a scatter plot.
    """
    if isinstance(df, pd.DataFrame):
        fig, ax = plt.subplots()
        groups = df.groupby(label)

        for name, points in groups:
            ax.scatter(points["component 0"], points["component 1"], label=name)

        ax.legend()
        plt.show()
    else:
        raise TypeError("input type is to be have to DataFrame")
