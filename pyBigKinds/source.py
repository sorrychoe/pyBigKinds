import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["일자", "언론사", "제목", "키워드"]
_ID_COLUMN = "뉴스 식별자"
_FALLBACK_KEY = ["일자", "언론사", "제목"]


def read_bigkinds(sources):
    """
    Reads one or more BigKinds xlsx exports into a single DataFrame.

    BigKinds exports at most 20,000 articles per file, so larger studies are split into
    several files. Files are validated one by one, concatenated, and articles that appear in
    more than one file are dropped (keyed on '뉴스 식별자' when every file has it, otherwise
    on '일자', '언론사', '제목'). The first occurrence is kept.

    Parameters:
    sources (str, path-like, file-like, DataFrame, or list of them): xlsx path(s), uploaded
        buffer(s), or already-loaded BigKinds DataFrame(s).

    Returns:
    pandas.DataFrame: Articles with at least '일자', '언론사', '제목', '키워드' columns.

    Raises:
    ValueError: If no source is given or a file misses required columns.
    """
    if not isinstance(sources, (list, tuple)):
        sources = [sources]
    if not sources:
        raise ValueError("no BigKinds file given")

    frames = []
    for i, src in enumerate(sources):
        # '뉴스 식별자' (e.g. '01100801.20230531232402001') must stay text: as a float it loses
        # precision and distinct articles collide, so deduplication would drop real rows.
        df = src if isinstance(src, pd.DataFrame) else pd.read_excel(src, dtype={_ID_COLUMN: str})
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            name = getattr(src, "name", None) or (src if isinstance(src, str) else f"file #{i + 1}")
            raise ValueError(f"{name}: missing BigKinds columns: {missing}")
        frames.append(df)

    # caller-loaded DataFrames may carry float-mangled ids; only trust text ids as the key
    use_id = all(
        _ID_COLUMN in df.columns
        and not pd.api.types.is_numeric_dtype(df[_ID_COLUMN])
        for df in frames
    )
    key = [_ID_COLUMN] if use_id else _FALLBACK_KEY
    merged = pd.concat(frames, ignore_index=True)
    result = merged.drop_duplicates(subset=key, keep="first").reset_index(drop=True)
    logger.info(
        "read %d file(s): %d rows, %d duplicate(s) removed by %s",
        len(frames), len(result), len(merged) - len(result), key,
    )
    return result
