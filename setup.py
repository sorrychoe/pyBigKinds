from os import path

from setuptools import find_packages
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="BigKindsParser",
    version="0.1.4",
    packages=find_packages("BigKindsParser"),
    package_dir={"": "bigkindsparser"},
    python_requires=">=3.8",
    author="sorrychoe",
    author_email="cjssoote@gmail.com",
    description=("Exploratory data analysis Toolkit of Python for BigKinds Data"),
    keywords=["Journalism", "BigKinds"],
    url="https://github.com/sorrychoe/BigKindsParser",
    license="MIT",
    install_requires=[
        "matplotlib>=3.5.3",
        "pandas==1.5.1",
        "wordcloud >= 1.8.2.2",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
