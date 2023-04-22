from setuptools import setup

setup(
    name="BigKindsParser",
    version="0.1.4",
    author="sorrychoe",
    author_email="cjssoote@gmail.com",
    description=("Exploratory data analysis Toolkit of Python for BigKinds Data"),
    license="MIT",
    keywords="Bigkinds",
    install_requires=[
        "matplotlib>=1.5.1",
        "pandas>=0.17.1",
        "wordcloud >= 1.8.2.2",
    ],
    packages=["BigKindsParser"],
)
