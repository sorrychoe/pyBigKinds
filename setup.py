from setuptools import setup, find_packages

setup(name='bigkindsparser', 

version='0.1.4',

description='본 패키지는 bigkinds에서 추출한 데이터셋을 간편하게 분석할 수 있도록 하는 패키지이다.',

author='sorrychoe',

author_email='cjssoote@gmail.com',

license='MIT', 

py_modules=['pandas', 'matplotlib', 'wordcloud'], # 패키지에 포함되는 모듈

python_requires='>=3.7',

install_requires=['pandas', 'matplotlib', 'wordcloud'], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=['bigkindsparser'] # 패키지가 들어있는 폴더들

)