import matplotlib.pyplot as plt
import wordcloud
from preprocessing import (
    counter_to_DataFrame,
    duplication_remover,
    keyword_parser,
    keywords_list,
    word_counter,
)


def press_keywords_wordcloud(df, press):
    """pipeline set"""
    df_keywords = df[df["언론사"].str.contains(press)]["키워드"]
    keywords = keywords_list(df_keywords)
    news_key = keyword_parser(keywords)
    news_key = duplication_remover(news_key)
    key = word_counter(news_key)
    news_key = counter_to_DataFrame(key)
    wc = wordcloud.WordCloud(
        font_path="./NanumBarunGothic.ttf",
        width=500,
        height=500,
        background_color="white",
    ).generate_from_frequencies(news_key.set_index("단어").to_dict()["빈도"])

    plt.imshow(wc)
    plt.axis("off")
    plt.show()
