#!/usr/bin/env python
# coding: utf-8
# %%
from sklearn.manifold import TSNE 
from sklearn.decomposition import PCA 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import pandas as pd 
import datetime
from gensim.models import KeyedVectors
# %matplotlib inline


# %%
model_name = '../_model/2020_10_29_194711[word2vec]'

# %%
mpl.rcParams['axes.unicode_minus'] = False 
plt.rc('font', family='D2Coding') 
def show_tsne(): 
    tsne = TSNE(n_components=2) 
    X = tsne.fit_transform(X_show) 
    df = pd.DataFrame(X, index=vocab_show, columns=['x', 'y']) 
    fig = plt.figure() 
    fig.set_size_inches(30, 20) 
    ax = fig.add_subplot(1, 1, 1) 
    ax.scatter(df['x'], df['y']) 
    for word, pos in df.iterrows(): 
        ax.annotate(word, pos, fontsize=10) 
        
    plt.xlabel("t-SNE 특성 0") 
    plt.ylabel("t-SNE 특성 1") 
    plt.savefig('../_output/word2vec.png', pad_inches=0.1)
    plt.show()
    
    
    return plt

# %%
model = KeyedVectors.load_word2vec_format(model_name)

vocab = list(model.wv.vocab) 
X = model[vocab]

sz = 500
X_show = X[:sz,:] 
vocab_show = vocab[:sz] 

plt = show_tsne()


# %%
def wc_to_file(wc):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d-%H%M%S')
    wc.to_file('../_output/' + 'wc_[' + date + '].png')


# %%
def wordcloud(noun_list):

    wc = WordCloud(font_path='font/NanumGothic.ttf', \
        background_color="white", \
        width=1000, \
        height=1000, \
        max_words=100, \
        max_font_size=300)

    wc.generate_from_frequencies(dict(noun_list))
    return wc


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
