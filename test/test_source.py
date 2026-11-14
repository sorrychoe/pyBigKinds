import io

import pandas as pd
import pytest

from pyBigKinds import read_bigkinds

PATH = "test/test.xlsx"


def _write(df, path):
    df.to_excel(path, index=False)
    return str(path)


def test_single_path():
    df = read_bigkinds(PATH)
    assert df.shape[0] == 31
    for col in ("일자", "언론사", "제목", "키워드"):
        assert col in df.columns


def test_buffer():
    with open(PATH, "rb") as f:
        buf = io.BytesIO(f.read())
    assert read_bigkinds(buf).shape[0] == 31


def test_distinct_files_are_concatenated(tmp_path):
    df = pd.read_excel(PATH)
    a = _write(df.iloc[:10], tmp_path / "a.xlsx")
    b = _write(df.iloc[10:], tmp_path / "b.xlsx")
    assert read_bigkinds([a, b]).shape[0] == 31


def test_overlap_is_dropped(tmp_path):
    df = pd.read_excel(PATH)
    a = _write(df.iloc[:20], tmp_path / "a.xlsx")
    b = _write(df.iloc[15:], tmp_path / "b.xlsx")
    assert read_bigkinds([a, b]).shape[0] == 31
    assert read_bigkinds([PATH, PATH]).shape[0] == 31


def test_news_id_is_preferred_key(tmp_path):
    df = pd.read_excel(PATH).iloc[:2].copy()
    df["제목"] = "same"
    df["일자"] = 20200101
    df["언론사"] = "same"
    df["뉴스 식별자"] = ["id1", "id2"]
    # identical by the fallback key, distinct by news id -> both kept
    assert read_bigkinds(_write(df, tmp_path / "a.xlsx")).shape[0] == 2


def test_missing_column_names_the_file(tmp_path):
    bad = _write(pd.read_excel(PATH).drop(columns="키워드"), tmp_path / "bad.xlsx")
    with pytest.raises(ValueError, match="bad.xlsx.*키워드"):
        read_bigkinds([PATH, bad])


def test_empty_list():
    with pytest.raises(ValueError):
        read_bigkinds([])


def test_dataframes_are_accepted():
    df = pd.read_excel(PATH)
    assert read_bigkinds([df.iloc[:20], df.iloc[15:]]).shape[0] == 31


def test_news_id_is_read_as_text(tmp_path):
    # real BigKinds ids; as floats both become 1.100101e+06 and would collide
    df = pd.read_excel(PATH).iloc[:2].copy()
    df["뉴스 식별자"] = ["01100101.20230501000000001", "01100101.20230501000000002"]
    df["제목"] = "same"
    df["일자"] = 20200101
    df["언론사"] = "same"
    out = read_bigkinds(_write(df, tmp_path / "a.xlsx"))
    assert out.shape[0] == 2
    assert out["뉴스 식별자"].tolist() == df["뉴스 식별자"].tolist()


def test_numeric_ids_fall_back_to_title_key():
    df = pd.read_excel(PATH)
    df["뉴스 식별자"] = 1.100101e06  # float-mangled: every row "collides"
    assert read_bigkinds(df).shape[0] == 31


def test_sample_export_keeps_every_article():
    df = read_bigkinds("data/president_yoon_2023_05.xlsx")
    assert df.shape[0] == 3744
