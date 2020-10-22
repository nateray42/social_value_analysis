#!/usr/bin/env python
# coding: utf-8
# %%
import requests
import re
import datetime
import pandas as pd
import sys

sys.path.append('..\\_system')
from basic_system import query_yes_no

from bs4 import BeautifulSoup
from tqdm import notebook


# %%
def hani_search(keyword, tf):
    
    url = 'http://search.hani.co.kr/Search?command=query&media=news&sort=d&period=year&'
    column_names = ['Link', 'Title', 'Article']
    df = pd.DataFrame(columns = column_names)
    index = df.index
    index.name = keyword

    for page in notebook.tqdm(range(50)):
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
                
    save_func(df) if tf is True
        
    return df


# %%
def joins_search(keyword, tf):
    
    url = 'http://news.joins.com/Search/News?&SortType=New&IsDuplicate=False'
    column_names = ['Link', 'Title', 'Article']
    df = pd.DataFrame(columns = column_names)
    index = df.index
    index.name = keyword

    for page in notebook.tqdm(range(50)):
        req_params = {
            'Keyword': keyword,
            'Page': page,
            'StartSearchDate': '2020.01.01',
            'SearchCategoryType': 'JoongangNews'
            }
        response = requests.get(url, params=req_params)
        html = response.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        results = soup.select('ul.list_default li h2 a')
        banned_list = ['[',']']
        
        for link in results:
            d = {}
            d['Link'] = link.get('href')
            d['Title'] = link.text
            d['Article'] = joins_article(d['Link'])
            #특정 기사 제외
            if all(x not in link.text for x in banned_list):
                df_length = len(df)
                df.loc[df_length] = d
                
    save_func(df) if tf else tf
        
    return df


# %%
def hani_article(url):
    response = requests.get(url, verify=False)
    html = response.text.strip()
    soup = BeautifulSoup(html, 'lxml')
    
    # 한겨례 기사 크롤링
    raw = soup.select('div.article-text div.text')[0]
    if raw.find('strong') is not None:
        unwanted = raw.find('strong')
        unwanted.extract()
        
    article = raw.text.strip()
    article = clean_text(article)
    return article


# %%
def joins_article(url):
    response = requests.get(url, verify=False)
    html = response.text.strip()
    soup = BeautifulSoup(html, 'lxml')
    
    # 중앙일보 기사 크롤링
    raw = soup.select('div.article_body')[0]
    if raw.find('strong') is not None:
        unwanted = raw.find('strong')
        unwanted.extract()
        
    article = raw.text.strip()
    article = clean_text(article)
    return article

# %%
# def agent_selector(agent):
#     dict agent_list:
#         # 한겨레 신문사 검색 URL
#         return url


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
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    title = df.index.name
    df.to_csv('../_Data/' + date + '[' + title + ']' + '.csv')

# %%
# if __name__ == '__main__':
#     agent = input('[!] 언론사 입력 : ')
#     keyword = input('[!] 검색어 입력 : ')
#     save_tf = '[!] csv로 저장할래? : '
#     tf = query_yes_no(save_tf)
#     main_search(agent, keyword, tf)


# %%
keyword = input('[!] 검색어 입력 : ')
save_tf = '[!] csv로 저장할래? : '
tf = query_yes_no(save_tf)
hani_search(keyword, tf)

# %%
keyword = input('[!] 검색어 입력 : ')
save_tf = '[!] csv로 저장할래? : '
tf = query_yes_no(save_tf)
joins_search(keyword, tf)
print('작업 완료했어~')

 # %%
 df.head()
