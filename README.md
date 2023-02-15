# BigKindsParser

BigKinds 데이터 전처리 자동화를 위한 모듈입니다. 

현재 지속적으록 개발 시도 중에 있으며, 향후 추가되어 완성되는 영역이 있으면 지속적으로 업로드할 계획입니다.

ver 0.1.4

</br>
</hr>

## 내장된 함수 목록
```
press_counter(dataframe)
```
> 입력한 데이터에서 언론사 별 보도 빈도를 따로 추출한 DataFrame으로 변환
</br>

```
keywords_list(dataframe)
```
> 입력한 데이터에서 기사 별 키워드를 list 형태로 변환
</br>

```
keyword_parser(list)
```
> 입력한 데이터에서 키워드를 파싱한 형태의 list로 반환
</br>

```
duplication_remover(list)
```
> 키워드 리스트에서 중복값을 제거한 list로 반환
</br>

```
word_counter(list)
```
> 키워드 리스트에서 단어의 빈도를 따로 추출한 Dictionary으로 변환
</br>

```
counter_to_DataFrame(dict)
```
> 키워드 빈도 Dictionary를 데이터 프레임의 형태로 변환
</br>

```
press_keywords_wordcloud(df, press)
```
> 입력한 언론사의 키워드 워드클라우드를 변환/출력
</br>
</hr>


