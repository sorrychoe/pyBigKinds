import pandas as pd
import pytest

from pyBigKinds import *


@pytest.fixture(scope="module")
def vector():
    df = pd.read_excel("test/test.xlsx")
    vector = tfidf_vector(df)
    return vector


def test_keywords_wordcloud(vector):
    with pytest.raises(TypeError):
        keywords_wordcloud(vector, "press")


def test_top_words(vector):
    with pytest.raises(TypeError):
        top_words(vector, "press")


def test_scatterplot(vector):
    with pytest.raises(TypeError):
        scatterplot(vector, "label")


@pytest.fixture(scope="module")
def dataframe():
    return pd.read_excel("test/test.xlsx")


def test_show_false_returns_figure(dataframe, monkeypatch):
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure

    def fail():
        raise AssertionError("plt.show must not be called")

    monkeypatch.setattr(plt, "show", fail)
    assert isinstance(top_words(dataframe, "경향", show=False), Figure)
    assert isinstance(keywords_wordcloud(dataframe, "경향신문", show=False), Figure)
    points = pd.DataFrame({"component 0": [0, 1], "component 1": [1, 0], "g": [0, 1]})
    assert isinstance(scatterplot(points, "g", show=False), Figure)
    plt.close("all")
