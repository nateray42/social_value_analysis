#!/usr/bin/env python
# coding: utf-8
# %%
import requests
import re
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import notebook


# %%
def main_search(keyword):
    # 한겨레 신문사 검색 URL
    url = 'http://search.hani.co.kr/Search?command=query&media=news&sort=d&period=all&'
    column_names = ['Link', 'Title', 'Article']
    df = pd.DataFrame(columns = column_names)
    index = df.index
    index.name = keyword

    for page in notebook.tqdm(range(20)):
        req_params = {
            'keyword': keyword,
            'pageseq': page
            }
        response = requests.get(url, params=req_params)
        html = response.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        results = soup.select('ul.search-result-list li dt a')
        banned_list = ['인사', '알림', '[']
        
        for link in results:
            d = {}
            d['Link'] = 'http:' + link.get('href')
            d['Title'] = link.text
            d['Article'] = hani_article(d['Link'])
            #특정 기사 제외
            if all(x not in link.text for x in banned_list):
                df_length = len(df)
                df.loc[df_length] = d
    return df


# %%
def hani_article(url):
    # 한겨례 기사 크롤링
    response = requests.get(url, verify=False)
    html = response.text.strip()
    soup = BeautifulSoup(html, 'lxml')
    raw = soup.select('div.article-text div.text')[0]
    if raw.find('strong') is not None:
        unwanted = raw.find('strong')
        unwanted.extract()
    article = raw.text.strip()
    article = clean_text(article)
    return article


# %%
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^·\-_+<>▶▽△▲⊙♡◀※◇■━◎○@\#$%&\\\=\(\'\"ⓒ(\n)(\t)‘’“”〃]', ' ', cleaned_text)
    cleaned_text = re.sub('㎢㈜', ' ', cleaned_text)
    cleaned_text = cleaned_text.replace("🇲\u200b🇮\u200b🇱\u200b🇱\u200b🇮\u200b🇪\u200b", "")
    output = ' '.join(cleaned_text.split())
    return output


# %%
def save_func(df):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d')
    title = df.index.name
    df.to_csv('../_Data/' + date + '[' + title + ']' + '.csv')


# %%
#if __name__ == '__main__':
    #main_search('사회적 가치 기업')


# %%
df = main_search('기업 사회적 가치')


# %%
save_func(df)

# %%
