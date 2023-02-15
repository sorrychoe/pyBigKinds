def press_counter(f): #언론사 별 보도 빈도 
    freq = df['언론사'].value_counts() 
    brod_df = pd.DataFrame(freq).reset_index() 
    brod_df.rename(columns = {'index':'언론사', '언론사':'기사'}, inplace = True) 
    return brod_df

def keywords_list(df): #키워드를 list로 변환
    return df['키워드'].values.tolist()

def keyword_parser(text_list): #키워드 파싱
    news_key = []
    for word in text_list:
        word = word.split(',') #',' 기점으로 스트링 분리
        news_key.append(word) #분리된 단어들을 리스트에 새로 정렬
    return news_key

def duplication_remover(news_key): #중복 값 제거
    news_value = []
    for j in news_key:
      j = list(set(j)) #중복 제거
      news_value.append(j) #제거된 리스트를 새로운 리스트에 삽입
    return news_value

def word_counter(news_value): #단어 갯수 카운트
    key_words = {}
    for k in range(len(news_value)):
          for i in news_value[k]:
              if i not in key_words:
                  key_words[i] = 1 #최초 언어
              elif i in key_words:
                  key_words[i] += 1 #중복 언어
    return key_words

def counter_to_DataFrame(key_words): #counter dict --> dataframe
    word_df = pd.DataFrame(key_words.items())
    word_df.columns = ['단어', '빈도']
    word_df = word_df.sort_values(['빈도'],ascending = False).reset_index(drop = True) #내림차순 정렬
    return word_df

def press_keywords_wordcloud(df, press): #pipeline set
    df_keywords = df[df['언론사'].str.contains(press)]['키워드'] #언론사 별 키워드를바로 워드클라우드로 전환
    keywords = keywords_list(df_keywords)
    news_key = keyword_parser(keywords)
    news_key = duplication_remover(news_key)
    key = word_counter(news_key)
    news_key = counter_to_DataFrame(key)
    wc = WordCloud(font_path = './NanumBarunGothic.ttf', #본인이 선호하는 폰트 설정
                    width = 500,
                    height = 500,
                    background_color='white').generate_from_frequencies(news_key.set_index('단어').to_dict()["빈도"])

    plt.imshow(wc)
    plt.axis('off')
    plt.show() # 워드클라우드 출력
    
