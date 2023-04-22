import matplotlib as plt
import pandas as pd
import wordcloud


class BigKinds():
    def __init__(self, data_path = None):
        self.data = pd.read_excel(data_path)   
        self.texts = self.data["키워드"].values.tolist()  
        

    def press_counter(self, data):
        """
        언론사 별 보도 빈도
        """
        freq = data["언론사"].value_counts()
        brod_df = pd.DataFrame(freq).reset_index()
        brod_df.rename(columns={"index": "언론사", "언론사": "기사"}, inplace=True)
        
        plt.bar(data = brod_df, x = '기사', y = '언론사')

        plt.figure(facecolor = 'white')
        plt.show()  


    def keyword_counter(self,texts):
        """
        키워드 절대 빈도
        """
        news_key = []
        for word in texts:
            word = word.split(",")  # ',' 기점으로 스트링 분리
            news_key.append(word)  # 분리된 단어들을 리스트에 새로 정렬
        key_words = {}
        for k in range(len(news_key)):
            for i in news_key[k]:
                if i not in key_words:
                    key_words[i] = 1  # 최초 언어
                elif i in key_words:
                    key_words[i] += 1  # 중복 언어
        word_df = pd.DataFrame(key_words.items())
        word_df.columns = ["단어", "빈도"]
        word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(drop=True)  # 내림차순 정렬
        return word_df


    def keyword_counter_no_duplicated(texts):
        """
        기사 별 중복 값 제거한 절대 빈도 반환
        """
        news_key = []
        for word in texts:
            word = word.split(",")  # ',' 기점으로 스트링 분리
            news_key.append(word)  # 분리된 단어들을 리스트에 새로 정렬
        news_value = []
        for j in news_key:
            j = list(set(j))  # 중복 제거
            news_value.append(j)  # 제거된 리스트를 새로운 리스트에 삽입
        key_words = {}
        for k in range(len(news_value)):
            for i in news_value[k]:
                if i not in key_words:
                    key_words[i] = 1  # 최초 언어
                elif i in key_words:
                    key_words[i] += 1  # 중복 언어
        word_df = pd.DataFrame(key_words.items())
        word_df.columns = ["단어", "빈도"]
        word_df = word_df.sort_values(["빈도"], ascending=False).reset_index(drop=True)  # 내림차순 정렬
        return word_df

    def press_keywords_wordcloud(self, texts):
        """
        make keyword wordcloud
        """
        words = self.keyword_counter_no_duplicated(texts)
        
        wc = wordcloud.WordCloud(
            font_path="font/NanumGothic.ttf", width=500, height=500, background_color="white"
        ).generate_from_frequencies(words.set_index("단어").to_dict()["빈도"])

        plt.imshow(wc)
        plt.axis("off")
        plt.show()  # 워드클라우드 출력
