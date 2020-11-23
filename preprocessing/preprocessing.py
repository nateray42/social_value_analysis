#!/usr/bin/env python
# coding: utf-8
# %%
import sys
import datetime
import re
from pathlib import Path
from tqdm import notebook
import pandas as pd
from eunjeon import Mecab
from collections import Counter

mecab = Mecab()


# %%
def df_to_text(df):
    text = df['article'].str.cat(sep=' ')
    return text


# %%
def text_to_file(text):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    f = open('../_Data/preprocessed/' + date + '.txt', "w", -1, 'utf-8')
    f.write(str(text))
    f.close()


# %%
def list_to_file(text):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    with open('../_Data/preprocessed/' + date + '.txt', "w", -1, 'utf-8') as f:
        [f.write(str(line)) for line in text]


# %%
def data_mainbus(mb):
    dlist = pd.read_csv('../_system/file_list.csv')
    for line in dlist['fname']:
        csv = Path("../_Data/" + line)
        if csv.is_file():
            df = pd.read_csv("../_Data/" + line)
            mb = pd.concat([mb, df], ignore_index = True)
#             mb.drop_duplicates(subset=['title'], inplace = True)
            mb.dropna(inplace = True)
    return mb


# %%
def corpus(text):
    corpus = []
    stopwords = open('../_system/stopwords.txt', 'r', encoding='utf-8').read()
    for sentence in notebook.tqdm(text):
            temp = mecab.nouns(sentence)
            temp = [word for word in temp if not word in stopwords]
            corpus.append(temp)
    return corpus


# %%
def store_data(df):
    for agent in df['agent'].unique():
        df_agent = agent_slice(df, agent)
        df_agent.to_csv('../_data/storage/' + agent + '.csv', index = False)


# %%

# %%
df = pd.DataFrame(columns = ['agent','link','title','article'])

# %%
df = data_mainbus(df)

# %%

# %%
khan = pd.read_csv('../_data/storage/경향.csv')

# %%
text = df_to_text(khan)


# %%
def text_to_lines(text):
    text = re.sub('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', '\n', text)
    text = re.sub('[.]', ' ', text)
    return text


# %%
text = text_to_lines(text)

# %%
text_to_file(text)

# %%
banned_list = ['기자', '제공', '사진', '무단', '전재', '재배포', '그래픽', '뉴스']


# %%
def delete_lines(fname):
    text = []
    with open(fname, 'r', encoding='utf-8') as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if all(banned_list not in line for banned_list in banned_list):
                text.append(line)
    list_to_file(text)
    return text


# %%
text = delete_lines('../_data/preprocessed/2020_11_23_015310.txt')

# %%
# def data_tokenizer(df):
#     text = df_to_text(df)
#     fname = text_to_files(text)
#     text = delete_lines('../_data/preprocessed/2020_11_20_155825[text].txt')

# %%
corpus_fname = '../_data/preprocessed/2020_11_23_015333.txt'

noun_corpus = []
with open(corpus_fname, 'r', encoding = 'utf-8') as f:
    for line in notebook.tqdm(f):
        try:
            nouns = mecab.nouns(line)
            noun_corpus.append(' '.join(nouns))
        except:
            continue

# %%
text = '\n'.join(noun_corpus)

# %%
list_to_file(text)

# %%
corpus_fname = '../_data/preprocessed/2020_11_20_160057[text].txt'
text = open(corpus_fname, 'r', encoding='utf-8').readlines()

# %%
corpus = [mecab.morphs(sent) for sent in notebook.tqdm(text)]

# %%
corpus = [mecab.nouns(sent) for sent in notebook.tqdm(text)]

# %%
text_to_file(corpus)

# %%
