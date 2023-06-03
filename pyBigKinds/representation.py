# pylint: disable=E0601,W0612

import gensim
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans

from .base import keyword_list


def kmeans(vec, k, random_state=None):
    """K-Means"""
    kmeans_model = KMeans(n_clusters=k, max_iter=1000, random_state=random_state).fit(
        vec,
    )
    return kmeans_model.predict(vec)


def dbscan(vec, eps, min_samples, metric="euclidian"):
    """DBSCAN"""
    dbscan_model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    return dbscan_model.fit_predict(vec)


def lda(df, num_topic=5, passes=10, iterations=50):
    """topic modeling"""
    news_words = keyword_list(df)
    news_dict = gensim.corpora.Dictionary(news_words)
    corpus = [news_dict.doc2bow(text) for text in news_words]

    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus,
        num_topics=num_topic,
        id2word=news_dict,
        passes=passes,
        iterations=iterations,
    )

    topic_table = pd.DataFrame()

    for i, topic_list in enumerate(ldamodel[corpus]):
        doc = topic_list[0] if ldamodel.per_word_topics else topic_list
        doc = sorted(doc, key=lambda x: (x[1]), reverse=True)

        for j, (topic_num, prop_topic) in enumerate(doc):
            if j == 0:
                topic_table = topic_table.append(
                    pd.Series([int(topic_num), round(prop_topic, 4), topic_list]),
                    ignore_index=True,
                )
            else:
                break

    topictable = topictable.reset_index()
    topictable.columns = ["뉴스 번호", "주요 토픽", "주요 토픽 비중", "토픽 별 비중"]
    return topic_table
