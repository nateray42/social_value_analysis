#!/usr/bin/env python
# coding: utf-8
# %%
import gensim
model = gensim.models.Word2Vec.load('../_Data/word2vec/ko.bin')


# %%
f = open("../_Data/2020_10_21-123259.txt", 'r', -1, 'utf-8')
data = f.read()
print(data)
f.close()


# %%
model.wv.vectors.shape


# %%
print(model.wv.most_similar("기업"))

