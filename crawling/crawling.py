#!/usr/bin/env python
# coding: utf-8
# %%
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# %%
import requests
import re
import datetime
import pandas as pd
import sys

sys.path.append('..//_system')
from basic_system import query_yes_no

from bs4 import BeautifulSoup
from tqdm import notebook


# %%
def main_search(agent, keyword, pages, tf):
    column_names = ['agent', 'link', 'title', 'article']
    df = pd.DataFrame(columns = column_names)
    index = df.index
    index.name = keyword
    
    if agent == '한겨레':
        df = hani_search(keyword, pages)
    elif agent == '중앙':
        df = joins_search(keyword, pages)
    elif agent == '한경':
        df = hnky_search(keyword, pages)
    else:
        print('다시 입력해줘~')
    
    df['agent'] = agent
    save_func(df, agent) if tf else tf


# %%
#한겨레
def hani_search(keyword, pages):
    
    url = 'http://search.hani.co.kr/Search?command=query&media=news&sort=s&period=year&'
    
    for page in notebook.tqdm(range(int(pages))):
        try:
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
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
                
    return df


# %%
#중앙일보
def joins_search(keyword, pages):
    
    url = 'http://news.joins.com/Search/TotalNews?'

    for page in notebook.tqdm(range(int(pages))):
        try:
            req_params = {
                'keyword': '기업 환경',
                'Page': page,
                'StartSearchDate': '2020.01.01',
                'SortType' : 'Accuracy',
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
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"

        
    return df


# %%
#한경
def hnky_search(keyword, pages):
    
    url = 'http://search.hankyung.com/apps.frm/search.news?&sort=RANK%2FDESC%2CDATE%2FDESC&'
    
    for page in notebook.tqdm(range(int(pages))):
        try:
            req_params = {
                'query': keyword,
                'page': page,
                'period': 'YEAR'
                }
            response = requests.get(url, params=req_params)
            html = response.text.strip()
            soup = BeautifulSoup(html, 'lxml')
            results = soup.select('div.txt_wrap > a')
            banned_list = ['의 국감', '신설법인', '종합']

            for link in results :
                if 'www.hankyung.com/' in link.get('href'):
                    d = {}
                    d['Link'] = link.get('href')
                    d['Title'] = clean_text(link.text)
                    d['Article'] = hnky_article(d['Link'])
                    #특정 기사 제외
                    if all(x not in link.text for x in banned_list):
                        df_length = len(df)
                        df.loc[df_length] = d
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
        
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
def hnky_article(url):
    response = requests.get(url, verify=False)
    html = response.text.strip()
    soup = BeautifulSoup(html, 'lxml')
    
    # 한경 기사 크롤링
    raw = soup.select('#articletxt')[0]
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
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^·\-_+<>▶▽△▲⊙♡◀◆◈※◇■●━◎○@\#$%&\\\=\(\'\"ⓒ(\n)(\t)‘’“”〃]', ' ', cleaned_text)
    cleaned_text = re.sub('㎢㈜', ' ', cleaned_text)
    cleaned_text = cleaned_text.replace("🇲\u200b🇮\u200b🇱\u200b🇱\u200b🇮\u200b🇪\u200b", "")
    cleaned_text = cleaned_text.replace("한국경제TV, 무단 전재 및 재배포 금지", "")
    cleaned_text = cleaned_text.replace("이미지를 누르면 크게 볼 수 있습니다", "")
    output = ' '.join(cleaned_text.split())
    return output


# %%
def save_func(df, agent):
    dt = datetime.datetime.now()
    date = dt.strftime('%Y_%m_%d_%H%M%S')
    title = df.index.name
    df.to_csv('../_data/' + '[' + agent + ']' + date + '[' + title + ']' + '.csv')


# %%
if __name__ == '__main__':
    agent = input('[!] 언론사 입력 : ')
    keyword = input('[!] 검색어 입력 : ')
    pages = input('[!] 검색 페이지 수 : ')
    save_tf = '[!] csv로 저장할래? : '
    tf = query_yes_no(save_tf)
    main_search(agent, keyword, pages, tf)
    print('작업 완료했어~')

# %%
