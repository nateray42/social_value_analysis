#!/usr/bin/env python
# coding: utf-8
# %%
import sys
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from eunjeon import Mecab
from collections import Counter


# %%
# def df_concat(df_1, df_2):
#     df = pd.concat()
#     df.drop_duplicates(['Title'], keep='first', inplace = True, ignore_index = True)
#     return df

# %%
def df_to_text(df):
    text = df['article'].str.cat(sep=' ')
    return text


# %%
def tokenize(df):
    mecab = Mecab()
    tokenized_data = []
    #아래에 stopwords 추가 가능
    stopwords = ['기자', '한겨레'] 
    for sentence in df['article']:
        temp_X = mecab.nouns(sentence)
        temp_X = [word for word in temp_X if not word in stopwords]
        tokenized_data.append(temp_X)
    
    return tokenized_data


# %%
def get_noun(df):
    
    mecab = Mecab()
    text = df_to_text(df)
    noun = mecab.nouns(text)
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
    wc.to_file('../_output/' + 'wc_[' + date + '].png')


# %%
def text_to_file(text):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d-%H%M%S')
    f = open('../_Data/' + date + '.txt', "w", -1, 'utf-8')
    f.write(str(text))
    f.close()


# %%
df1 = pd.read_csv("../_Data/[중앙]2020_10_26_183435[기업 사회].csv")
df2 = pd.read_csv("../_Data/[한경]2020_10_26_184732[기업 사회].csv")
df3 = pd.read_csv("../_Data/[한겨레]2020_10_26_185605[기업 사회].csv")

# %%
df = pd.concat([df1, df2], ignore_index = True)

# %%
df = pd.concat([df, df3], ignore_index = True)

# %%
df.drop(columns=['Unnamed: 0'], inplace = True)

# %%
df.drop_duplicates(subset=['title'], inplace = True)

# %%
df.dropna(inplace = True)

# %%
noun_list = get_noun(df)
wc = visualize(noun_list)


# %%
wc_to_file(wc)

# %%
df['article'] = df['article'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

# %%
tokens = tokenize(df)

# %%
text_to_file(tokens)
