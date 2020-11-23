#!/usr/bin/env python
# coding: utf-8
# %%
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from tqdm import notebook
import datetime
from gensim.models import KeyedVectors
import pandas as pd

# %%
from eunjeon import Mecab

# %%
corpus_fname = '../_data/2020_11_17_150054.txt'

# %%
mecab = Mecab()


# %%
def save_model(model):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    model_fname = '../_model/' + date + '[word2vec]'
    model.wv.save_word2vec_format(model_fname)


# %%
class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subed = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1

# %%
# corpus = [sent.strip().split(' ') for sent in notebook.tqdm(open(corpus_fname, 'r', encoding='utf-8').readlines())]


# %%
text = open(corpus_fname, 'r', encoding='utf-8').readlines()

# %%
corpus = [mecab.morphs(sent) for sent in notebook.tqdm(text)]


# %%
stopwords = open('../_system/stopwords.txt', 'r', encoding='utf-8').read()

# %%
corpus = []
for sentence in notebook.tqdm(text):
        temp = mecab.nouns(sentence)
        temp = [word for word in temp if not word in stopwords]
        temp = [word for word in temp if len(word) > 1]
        corpus.append(temp)

# %%
model = Word2Vec(corpus, size=100, workers=4, sg=1, min_count=5, compute_loss=True, iter=10, callbacks=[callback()])

# %%
model = KeyedVectors.load_word2vec_format('../_model/2020_10_29_194711[word2vec]')

# %%
print(model)

# %%
model.wv.most_similar("기업", topn=5)[0][0]

# %%
model.wv.index2entity[:100]

# %%
save_model(model)

# %%
lists = ['기업', '이익', '환경', '인권', '노동']

# %%
df = pd.DataFrame(columns = ['keywords', '1st', '2nd', '3rd', '4th', '5th'])

for words in lists:    
    new = []
    new.append(str(words))
    for i in range(5):
        new.append(model.wv.most_similar(words, topn=5)[i][0])
    print(new)
    df_length = len(df)
    df.loc[df_length] = new

# %%
df


# %%
def save_func(self):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    fname = '[' + self.agent + ']' + date + '[' + self.keyword + ']'
    self.df.to_csv('../_data/' + fname + '.csv', index = False)
    df = pd.read_csv('../_system/file_list.csv')
    new = {}
    new['agent'] = self.agent
    new['keyword'] = self.keyword
    new['pages'] = self.page
    new['date'] = date
    new['fname'] = fname + '.csv'
    df_length = len(df)
    df.loc[df_length] = new
    df.to_csv('../_system/file_list.csv', index=False)
