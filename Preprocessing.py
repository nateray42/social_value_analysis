#!/usr/bin/env python
# coding: utf-8
# %%
import sys

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from eunjeon import Mecab
from collections import Counter


# %%
df = pd.read_csv("../_Data/2020_10_19[기업 사회적 가치].csv")

text = df['Article'].str.cat(sep=' ')


# %%
def get_noun(text):

    mecab = Mecab()
    noun = mecab.nouns(text)
    for i,v in enumerate(noun):
        if len(v) < 2:
            noun.pop(i)

    count = Counter(noun)
    noun_list = count.most_common(100)

    return noun_list


# %%
def visualize(noun_list):

    wc = WordCloud(font_path='font/NanumGothic.ttf', \
        background_color="white", \
        width=1000, \
        height=1000, \
        max_words=100, \
        max_font_size=300)

    wc.generate_from_frequencies(dict(noun_list))
    wc.to_file('keyword.png')


# %%
noun_list = get_noun(text)
visualize(noun_list)


# %%
