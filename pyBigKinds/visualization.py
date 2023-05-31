import platform

import matplotlib.pyplot as plt
import wordcloud

from .preprocessing import (
    counter_to_DataFrame,
    duplication_remover,
    keyword_parser,
    keywords_list,
    word_counter,
)

if platform.system() in ["Windows", "linux"]:
    plt.rcParams["font.family"] = "Malgun Gothic"
    font_path = 'malgun'

elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
    font_path = 'AppleGothic'

else:
    print("미지원 os입니다.")

plt.rcParams["axes.unicode_minus"] = False


def keywords_wordcloud(df, press):
    """언론사 별 키워드 워드클라우드 생성"""
    df_keywords = df[df["언론사"] == press]
    keywords = keywords_list(df_keywords)
    news_key = keyword_parser(keywords)
    news_key = duplication_remover(news_key)
    key = word_counter(news_key)
    news_key = counter_to_DataFrame(key)
    wc = wordcloud.WordCloud(
        font_path=font_path,
        width=500,
        height=500,
        background_color="white",
    ).generate_from_frequencies(news_key.set_index("단어").to_dict()["빈도"])

    plt.imshow(wc)
    plt.axis("off")
    plt.show()


def top_words(df, press):
    """언론사 별 사용 단어 빈도 상위 25개"""
    df_keywords = df[df["언론사"].str.contains(press)]
    keywords = keywords_list(df_keywords)
    news_key = keyword_parser(keywords)
    news_key = duplication_remover(news_key)
    key = word_counter(news_key)
    news_key = counter_to_DataFrame(key)

    data = news_key.head(25)
    plt.barh(data["단어"], data["빈도"].sort_values(ascending=True))
    plt.show()