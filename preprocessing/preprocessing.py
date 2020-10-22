#!/usr/bin/env python
# coding: utf-8
# %%
import sys
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Okt
from collections import Counter


# %%
def df_to_text(df):
    text = df['Article'].str.cat(sep=' ')
    return text


# %%
def tokenize(df):
    okt = Okt()
    tokenized_data = []
    #아래에 stopwords 추가 가능
    stopwords = ['기자', '한겨레','의','가','이','은','들','는','좀','잘','걍','과','도','을', '를','으로','자','에','와','한','하다'] 
    for sentence in df['Article']:
        temp_X = okt.morphs(sentence, stem=True)
        temp_X = [word for word in temp_X if not word in stopwords]
        tokenized_data.append(temp_X)
    
    return tokenized_data
    


# %%
def get_noun(df):
    
    okt = Okt()
    text = df_to_text(df)
    noun = okt.nouns(text)
    for i,v in enumerate(noun):
        if len(v) < 2:
            noun.pop(i)

    count = Counter(noun)
    noun_list = count.most_common(70)

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
    return wc


# %%
def wc_to_file(wc):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d-%H%M%S')
    wc.to_file('../_Outputs/' + 'wc_[' + date + '].png')


# %%
def text_to_file(text):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d-%H%M%S')
    f = open('../_Data/' + date + '.txt', "w", -1, 'utf-8')
    f.write(str(text))
    f.close()


# %%
df = pd.read_csv("../_Data/2020_10_21[기업 사회].csv")

# %%
noun_list = get_noun(df)
wc = visualize(noun_list)


# %%
wc_to_file(wc)

# %%
text = df_to_text(df)
text_to_file(text)

# %%
df['Article'] = df['Article'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

# %%
tokens = tokenize(df)

# %%
text_to_file(tokens)

# %%
