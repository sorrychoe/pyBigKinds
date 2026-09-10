# pyBigKinds

pyBigKinds는 한국 언론의 빅데이터 저장소인 BigKinds에서 추출한 데이터를 low-Code로 분석할 수 있게 만든 툴입니다.

## Requirements

- Python >= 3.10
- 한글 폰트: Windows(맑은 고딕)와 macOS(AppleGothic)는 기본 폰트를 사용합니다.
  Linux에서는 `NanumGothic`(예: `sudo apt-get install fonts-nanum`) 등 한글 폰트를
  설치해야 워드클라우드와 그래프의 한글이 정상 출력됩니다.

## Installation

- macOS

  ```bash
  python3 -m pip install pyBigKinds
  ```

- Windows, linux

  ```bash
  python -m pip install pyBigKinds
  ```

## Usage

```python
import pyBigKinds as bk

bk.press_counter(df)
```

![](https://github.com/sorrychoe/pyBigKinds/blob/release/docs/example1.png)

```python
import pyBigKinds as bk

bk.keywords_wordcloud(df, "중앙일보")
```

![](https://github.com/sorrychoe/pyBigKinds/blob/release/docs/example2.png)


## License

[MIT](https://choosealicense.com/licenses/mit/)

## you have some issue?

사용 중 문제 발생 시, 해당 Repo issue에 등록해주세요.
