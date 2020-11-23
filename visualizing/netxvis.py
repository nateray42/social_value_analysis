#!/usr/bin/env python
# coding: utf-8
# %%
import numpy as np
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt


# %%
from eunjeon import Mecab
mecab = Mecab()


# %%
# f = open('../_data/preprocessed/2020_11_19_142910[text].txt', 'r', encoding = 'utf-8')
# lines = f.readlines()
# f.close()


# %%
with open('../_data/preprocessed/donga.txt', 'r', encoding = 'utf-8') as f:
    lines = f.read().splitlines()
# lines
sentences = [line for line in lines if line != '']
tagged_sentences = [mecab.pos(sent) for sent in sentences]
tagged_sentences[:10]


# %%
f = open('../_system/stopwords.txt', 'r', encoding = 'utf-8')
stopwords = f.read().splitlines()
f.close()


# %%
f = open('../_system/whitelist.txt', 'r', encoding = 'utf-8')
whitelist = f.read().splitlines()
f.close()


# %%
dataset = []
for sent in tagged_sentences:   
    noun_list = []
    for word, tag in sent:
        if tag in ['NNP', 'NNG'] and len(word) > 1 and word in whitelist:
            noun_list.append(word)
    dataset.append(noun_list)
dataset[:10]


# %%
# dataset = []
# for i in range(len(lines)):
#     attr = mecab.nouns(re.sub('[^가-힣a-zA-Z\s]', '', lines[i]))
#     if len(attr) > 1 and attr not in stop_words:
#         dataset.append(attr)
# dataset[:10]


# %%
from apyori import apriori
result = (list(apriori(dataset, min_support = 0.0009)))
df = pd.DataFrame(result)
df['length'] = df['items'].apply(lambda x: len(x))
df = df[(df['length'] == 2) &
       (df['support'] >= 0.0009)].sort_values(by='support', ascending = False)
df.head(10)


# %%
df.to_csv('../_data/apiori.csv', index = False)

# %%
G = nx.Graph()
ar = (df['items']); G.add_edges_from(ar)


# %%
pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))


# %%
# pos = nx.planar_layout(G)
# pos = nx.circular_layout(G)
pos = nx.fruchterman_reingold_layout(G)
# pos = nx.spectral_layout(G)
# pos = nx.random_layout(G)
# pos = nx.shell_layout(G)


# %%
plt.figure(figsize = (16,12)); plt.axis('off')
nx.draw_networkx(G, font_family = 'Noto Sans CJK KR', font_size = 16,
                pos = pos, node_color = list(pr.values()), node_size = nsize,
                alpha = 0.7, edge_color = '.5', cmap = plt.cm.YlGn)
plt.savefig('../_output/networkx.png', bbox_inches = 'tight')


# %%




