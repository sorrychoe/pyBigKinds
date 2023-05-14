import pandas as pd


def press_counter(df):
    """언론사 별 보도 빈도"""
    freq = df["언론사"].value_counts()
    brod_df = pd.DataFrame(freq).reset_index()
    brod_df.rename(columns={"index": "언론사", "언론사": "기사"}, inplace=True)
    return brod_df


def header_remover(df):
    """[]로 표시된 헤더 삭제"""
    ans = df["제목"].str.replace("\[[^)]*\]", "")
    return ans


def day_range(df):
    """날짜 범위 파악"""
    print("first day: ", df["일자"].min(), "\n", "last day: ", df["일자"].max())


def keywords_list(df):
    """키워드를 list로 변환"""
    return df["키워드"].values.tolist()


def keyword_parser(text_list):
    """키워드 파싱"""
    news_key = []
    for word in text_list:
        word = word.split(",")
        news_key.append(word)
    return news_key


def duplication_remover(news_key):
    """중복 값 제거"""
    news_value = []
    for j in news_key:
        j = list(set(j))
        news_value.append(j)
    return news_value


def word_counter(news_value):
    """단어 갯수 카운트"""
    key_words = {}
    for k in range(len(news_value)):
        for i in news_value[k]:
            if i not in key_words:
                key_words[i] = 1
            elif i in key_words:
                key_words[i] += 1
    return key_words


def counter_to_DataFrame(key_words):
    """counter dict --> dataframe"""
    word_df = pd.DataFrame(key_words.items())
    word_df.columns = ["단어", "빈도"]
    word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(drop=True)  # 내림차순 정렬
    return word_df
