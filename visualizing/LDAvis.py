#!/usr/bin/env python
# coding: utf-8
# %%
corpus_path = '../_data/preprocessed/2020_11_19_142910[text].txt'

class Documents:
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for doc in f:
                yield doc.strip().split()

documents = Documents(corpus_path)


# %%
import pyLDAvis
import pickle
import gensim

from sklearn.feature_extraction.text import CountVectorizer
import codecs


# %%
dictionary = gensim.corpora.Dictionary(documents)
print('dictionary size : %d' % len(dictionary))


# %%
from collections import Counter

min_count = 50
word_counter = Counter((word for words in documents for word in words))
removal_word_idxs = {
    dictionary.token2id[word] for word, count in word_counter.items()
    if count < min_count
}

del_ids = [k for k,word in dictionary.items() if len(word) < 2 ]

dictionary.filter_tokens(removal_word_idxs)
dictionary.filter_tokens(bad_ids=del_ids)
dictionary.compactify()
print('dictionary size : %d' % len(dictionary))


# %%
class Corpus:
    def __init__(self, path, dictionary):
        self.path = path
        self.dictionary = dictionary
        self.length = 0
    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for doc in f:
                yield self.dictionary.doc2bow(doc.split())
    def __len__(self):
        if self.length == 0:
            with open(self.path, encoding='utf-8') as f:
                for i, doc in enumerate(f):
                    continue
            self.length = i + 1
        return self.length

corpus = Corpus(corpus_path, dictionary)
for i, doc in enumerate(corpus):
    if i >= 5: break
    print(doc)


# %%
from gensim.models import LdaModel

lda_model_path = '../_model/testLdaModel'

lda_model = LdaModel(corpus, id2word=dictionary, num_topics=50)
with open(lda_model_path, 'wb') as f:
    pickle.dump(lda_model, f)


# %%
def get_topic_term_prob(lda_model):
    topic_term_freqs = lda_model.state.get_lambda()
    topic_term_prob = topic_term_freqs / topic_term_freqs.sum(axis=1)[:, None]
    return topic_term_prob


# %%
print(lda_model.alpha.shape) # (n_topics,)
print(lda_model.alpha.sum()) # 1.0

topic_term_prob = get_topic_term_prob(lda_model)
print(topic_term_prob.shape)     # (n_topics, n_terms)
print(topic_term_prob[0].sum())  # 1.0


# %%
import pyLDAvis.gensim as gensimvis

prepared_data = gensimvis.prepare(lda_model, corpus, dictionary)


# %%
# pyLDAvis.display(prepared_data)


# %%
pyldavis_html_path = '../_output/pyLDAvis.html'
pyLDAvis.save_html(prepared_data, pyldavis_html_path)


# %%
