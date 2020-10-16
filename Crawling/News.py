#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import operator
import time
import datetime


# In[18]:


def main_search(keyword):
    # 한겨레 신문사 검색 URL
    url = 'http://search.hani.co.kr/Search?command=query&media=news&sort=d&period=all&'
    column_names = ['Link', 'Title', 'Article']
    df = pd.DataFrame(columns = column_names)
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d')

    for page in range(5):
        req_params = {
            'keyword': keyword,
            'pageseq': page
            }
        response = requests.get(url, params=req_params)
        html = response.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        results = soup.select('ul.search-result-list li dt a')
        for link in results:
            d = {}
            d['Link'] = 'http:' + link.get('href')
            d['Title'] = link.text
            d['Article'] = hani_article(d['Link'])
            #news_url = link.get('href') 
            #news_title = link.text 
            #print(news_url, news_title)
            #hani_article(news_url)
            df.append(d, ignore_index=True)
    df.to_csv(date + '[' + keyword + ']' + '.csv', header=False)
    return df


# In[19]:


def hani_article(url):
    response = requests.get(url, verify=False)
    html = response.text.strip()
    # print(html[:500])
    soup = BeautifulSoup(html, 'html5lib')
    raw = soup.select('div.article-text div.text')[0]
    if raw.find('strong') is not None:
        unwanted = raw.find('strong')
        unwanted.extract()
    article = raw.text.strip()
    article = clean_text(article)
    return article


# In[20]:


def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^·\-_+<>▶▽△▲⊙♡◀※◇■━@\#$%&\\\=\(\'\"ⓒ(\n)(\t)‘’“”]', ' ', cleaned_text)
    cleaned_text = cleaned_text.replace("🇲\u200b🇮\u200b🇱\u200b🇱\u200b🇮\u200b🇪\u200b", "")
    return cleaned_text


# In[21]:


#if __name__ == '__main__':
    #hani_search('사회적 가치 기업')


# In[22]:


main_search('기업 사회적 가치')


# In[23]:


df.head()


# In[ ]:




