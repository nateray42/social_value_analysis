#!/usr/bin/env python
# coding: utf-8
# %%
from sklearn.manifold import TSNE 
from sklearn.decomposition import PCA 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import pandas as pd 
from gensim.models import KeyedVectors


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
    plt.show()


# %%
model_name = '../_model/word2vec' 
model = KeyedVectors.load_word2vec_format(model_name)

vocab = list(model.wv.vocab) 
X = model[vocab]

sz = 500 
X_show = X[:sz,:] 
vocab_show = vocab[:sz] 

show_tsne()

