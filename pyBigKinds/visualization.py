# pylint: disable=W0612
import platform

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

if platform.system() in ["Windows", "Linux"]:
    plt.rcParams["font.family"] = "Malgun Gothic"
    font_path = "malgun"

elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
    font_path = "AppleGothic"

else:
    print("미지원 os입니다.")

plt.rcParams["axes.unicode_minus"] = False


def keywords_wordcloud(df, press):
    """언론사 별 키워드 워드클라우드 생성"""
    if isinstance(df, pd.DataFrame):
        df_keywords = df[df[press] == press]
        keywords = keyword_list(df_keywords)
        news_key = keyword_parser(keywords)
        news_key = duplication_remover(news_key)
        key = word_counter(news_key)
        news_key = counter_to_dataframe(key)
        wc = wordcloud.WordCloud(
            font_path=font_path,
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
    """언론사 별 사용 단어 빈도 상위 n개"""
    if isinstance(df, pd.DataFrame):
        df_keywords = df[df[press].str.contains(press)]
        keywords = keyword_list(df_keywords)
        news_key = keyword_parser(keywords)
        news_key = duplication_remover(news_key)
        key = word_counter(news_key)
        news_key = counter_to_dataframe(key)

        data = news_key.head(top_n)
        plt.barh(data["단어"], data["빈도"].sort_values(ascending=True))
        plt.show()
    else:
        raise TypeError("input type is to be have to DataFrame")


def scatterplot(df, label):
    """scatter plot for dimension reduction"""
    if isinstance(df, pd.DataFrame):
        fig, ax = plt.subplots()
        groups = df.groupby(label)

        for name, points in groups:
            ax.scatter(points["component 0"], points["component 1"], label=name)

        ax.legend()
        plt.show()
    else:
        raise TypeError("input type is to be have to DataFrame")
