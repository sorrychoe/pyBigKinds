import pandas as pd


def header_remover(df):
    """[]로 표시된 헤더 삭제"""
    if isinstance(df) != pd.DataFrame:
        raise TypeError("input type is to be have to DataFrame")
    ans = df["제목"].str.replace("\[[^)]*\]", "")
    return ans


def keyword_list(df):
    """키워드를 list로 변환"""
    if isinstance(df) != pd.DataFrame:
        raise TypeError("input type is to be have to DataFrame")
    return df["키워드"].values.tolist()


def keyword_parser(text_list):
    """키워드 파싱"""
    if isinstance(text_list) != list:
        raise TypeError("input type is to be have to list")
    news_key = []
    for word in text_list:
        if isinstance(word) != str:
            raise ValueError("input list is not valid format")
        word = word.split(",")
        news_key.append(word)
    return news_key


def duplication_remover(news_key):
    """중복 값 제거"""
    if isinstance(news_key) != list:
        raise TypeError("input type is to be have to list")
    news_value = []
    for j in news_key:
        if isinstance(j) != list:
            raise ValueError("input list is not valid format")
        j = list(set(j))
        news_value.append(j)
    return news_value


def word_counter(news_value):
    """단어 갯수 카운트"""
    if isinstance(news_value) != list:
        raise TypeError("input type is to be have to list")
    key_words = {}
    for k in range(len(news_value)):
        for i in news_value[k]:
            if i not in key_words:
                key_words[i] = 1
            elif i in key_words:
                key_words[i] += 1
    return key_words


def counter_to_dataframe(key_words):
    """counter dict --> dataframe"""
    if isinstance(key_words) != dict:
        raise TypeError("input type is to be have to dict")
    word_df = pd.DataFrame(key_words.items())
    word_df.columns = ["단어", "빈도"]
    word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(
        drop=True,
    )  # 내림차순 정렬
    return word_df
