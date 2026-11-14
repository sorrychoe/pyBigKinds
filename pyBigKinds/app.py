"""
No-code web app for BigKinds data. Run with ``pybigkinds app``.

Every computation calls a public pyBigKinds function, so anything done here can be
reproduced in Python code.
"""
# pylint: disable=C0103, C0116, C2401, W0621  # streamlit script: module-level state is intended
import importlib.util
import io

import pandas as pd
import streamlit as st

import pyBigKinds as bk

st.set_page_config(page_title="PyBigKinds", layout="wide")


@st.cache_data(show_spinner="파일을 읽는 중...")
def load(files):
    """files: tuple of (name, bytes). Returns (merged df, per-file row counts)."""
    frames, counts = [], []
    for name, data in files:
        buf = io.BytesIO(data)
        buf.name = name
        df = bk.read_bigkinds(buf)  # validates columns and names the bad file
        frames.append(df)
        counts.append({"파일": name, "기사": len(df)})
    return bk.read_bigkinds(frames), pd.DataFrame(counts)


def csv_button(df, file_name, key):
    # utf-8-sig so Excel opens Korean text correctly
    st.download_button(
        "CSV 다운로드", df.to_csv(index=False).encode("utf-8-sig"), file_name, "text/csv", key=key,
    )


def figure(fig, file_name, key):
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    st.download_button("PNG 다운로드", buf.getvalue(), file_name, "image/png", key=key)


# ---------- sidebar: data ----------
st.sidebar.title("PyBigKinds")
uploads = st.sidebar.file_uploader(
    "BigKinds xlsx (여러 개 가능)", type="xlsx", accept_multiple_files=True,
)

if uploads:
    try:
        data, counts = load(tuple((f.name, f.getvalue()) for f in uploads))
    except ValueError as e:
        st.sidebar.error(str(e))
        st.stop()
    st.session_state["data"] = data
    st.sidebar.dataframe(counts, hide_index=True)
    st.sidebar.caption(
        f"병합 {len(data):,}건 · 중복 제거 {int(counts['기사'].sum()) - len(data):,}건"
    )

if "data" not in st.session_state:
    st.title("BigKinds 뉴스 데이터 분석")
    st.info("왼쪽에서 BigKinds에서 내려받은 xlsx 파일을 올려주세요. 20,000건이 넘으면 기간을 나눠 여러 파일로 올리면 됩니다.")
    st.stop()

data = st.session_state["data"]
presses = sorted(data["언론사"].dropna().unique())
chosen = st.sidebar.multiselect("언론사 필터", presses, default=presses)
df = data[data["언론사"].isin(chosen)].reset_index(drop=True)
if df.empty:
    st.warning("선택된 언론사가 없습니다.")
    st.stop()

buf = io.BytesIO()
df.to_excel(buf, index=False)
st.sidebar.download_button("병합 데이터 xlsx", buf.getvalue(), "bigkinds_merged.xlsx")
csv_button(df, "bigkinds_merged.csv", "merged_csv")

has_ml = all(importlib.util.find_spec(m) for m in ("tomotopy", "mlxtend"))
overview, keywords, tfidf_tab, cluster, topic = st.tabs(
    ["개요", "키워드", "TF-IDF", "군집·차원축소", "토픽·연관"],
)

# ---------- overview ----------
with overview:
    first, last = bk.day_range(df)
    st.metric("기간", f"{first} ~ {last}")
    counter = bk.press_counter(df)
    st.bar_chart(counter.set_index("언론사"))
    st.dataframe(counter, hide_index=True)
    csv_button(counter, "press_counter.csv", "press_csv")

# ---------- keywords ----------
with keywords:
    per_doc = st.checkbox("기사 내 중복 키워드는 한 번만 세기", value=True)
    freq = bk.keyword_dataframe_no_duplicated(df) if per_doc else bk.keyword_dataframe(df)
    st.dataframe(freq, hide_index=True)
    csv_button(freq, "keywords.csv", "kw_csv")

    press = st.selectbox("언론사별 시각화", sorted(df["언론사"].unique()))
    top_n = st.slider("상위 단어 수", 5, 100, 25)
    left, right = st.columns(2)
    with left:
        figure(bk.top_words(df, press, top_n=top_n, show=False), "top_words.png", "top_png")
    with right:
        figure(bk.keywords_wordcloud(df, press, show=False), "wordcloud.png", "wc_png")

# ---------- tf-idf ----------
with tfidf_tab:
    scores = bk.tfidf(df)
    st.dataframe(scores, hide_index=True)
    csv_button(scores, "tfidf.csv", "tfidf_csv")

# ---------- clustering ----------
with cluster:
    method = st.radio("군집 방법", ["K-means", "DBSCAN"], horizontal=True)
    if method == "K-means":
        k = st.number_input("군집 수 (k)", 2, 50, 3)
    else:
        eps = st.number_input("eps", 0.01, 10.0, 0.5)
        min_samples = st.number_input("min_samples", 1, 100, 5)
    reducer = st.radio("차원축소", ["PCA", "t-SNE"], horizontal=True)

    if st.button("실행", key="run_cluster"):
        vec = bk.normalize_vector(bk.tfidf_vector(df))
        labels = bk.kmeans(vec, int(k)) if method == "K-means" else bk.dbscan(vec, eps, int(min_samples))
        points = bk.pca(vec) if reducer == "PCA" else bk.t_sne(vec, learning_rate=100)
        points["군집"] = labels
        figure(bk.scatterplot(points, "군집", show=False), "cluster.png", "cluster_png")
        result = df[["일자", "언론사", "제목"]].assign(군집=labels)
        st.dataframe(result, hide_index=True)
        csv_button(result, "clusters.csv", "cluster_csv")

# ---------- topic / association ----------
with topic:
    if not has_ml:
        st.info("이 탭은 추가 설치가 필요합니다: `pip install \"pyBigKinds[ml]\"`")
    else:
        st.subheader("LDA 토픽 모델링")
        topics_k = st.number_input("토픽 수", 2, 50, 10)
        if st.button("LDA 실행", key="run_lda"):
            model = bk.lda(df, k=int(topics_k))
            table = pd.DataFrame(
                {
                    f"토픽 {i}": [w for w, _ in model.get_topic_words(i, top_n=10)]
                    for i in range(model.k)
                },
            )
            st.dataframe(table, hide_index=True)
            csv_button(table, "lda_topics.csv", "lda_csv")

        st.subheader("연관 규칙")
        support = st.slider("최소 지지도 (min_support)", 0.05, 1.0, 0.5)
        if st.button("연관 규칙 실행", key="run_assoc"):
            try:
                rules = bk.association(df, min_support=support)
            except ValueError as e:
                st.warning(str(e))
            else:
                for col in ("antecedents", "consequents"):
                    rules[col] = rules[col].map(lambda s: ", ".join(sorted(s)))
                st.dataframe(rules, hide_index=True)
                csv_button(rules, "association.csv", "assoc_csv")
