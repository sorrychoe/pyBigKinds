# pylint: disable=F403
# pylint: disable=F405

import pandas as pd
import pytest

from pyBigKinds import *


@pytest.fixture(scope="module")
def dataframe():
    df = pd.read_excel("test/test.xlsx")
    return df


def test_header_remover(dataframe):
    ans = header_remover(dataframe)
    assert ans[0] == " 한반도 긴장 높인 북한의 군사정찰위성 발사 규탄한다"


def test_keyword_list(dataframe):
    assert type(keyword_list(dataframe)) is list


def test_keyword_parser(dataframe):
    word_list = keyword_parser(keyword_list(dataframe))
    assert type(word_list) is list
    assert type(word_list[1]) is list


def test_duplication_remover(dataframe):
    word_list = keyword_parser(keyword_list(dataframe))
    word_value = duplication_remover(word_list)
    assert word_value[4].count('남용') == 1


def test_word_counter(dataframe):
    word_list = keyword_parser(keyword_list(dataframe))
    word_value = duplication_remover(word_list)
    key_words = word_counter(word_value)
    assert key_words['남용'] == 4


def test_counter_to_dataframe(dataframe):
    word_list = keyword_parser(keyword_list(dataframe))
    word_value = duplication_remover(word_list)
    key_words = word_counter(word_value)
    data = counter_to_dataframe(key_words)

    assert data.columns[0] == '단어'
    assert data.columns[1] == '빈도'
    assert data['빈도'].max() == data['빈도'][0]
