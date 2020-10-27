#!/usr/bin/env python
# coding: utf-8
# %%
#https 오류 무시
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
#메인 검색 클래스
class Main_search:
    def __init__(self, keyword, page):
        self.keyword = keyword
        self.page = page
        self.whitelist = ''
        
    def search(self):
        column_names = ['agent', 'link', 'title', 'article']
        df = pd.DataFrame(columns = column_names)
        
        for page in notebook.tqdm(range(int(self.page))):
            try:
                parameter = self.parameter
                parameter[(list(parameter)[0])] = page
                response = requests.get(self.url, params = parameter)
                html = response.text.strip()
                soup = BeautifulSoup(html, 'lxml')
                results = soup.select(self.title_selector)

                for link in results:
                    
                    d = {}
                    d['agent'] = self.agent
                    d['link'] = link.get('href')
                    if self.whitelist in link.get('href'):
                        if 'http' not in d['link']:
                            d['link'] = 'http:' + d['link']
                        d['title'] = self.clean_text(link.text)
                        d['article'] = self.find_article(d['link'])

                        if all(x not in link.text for x in self.banned_list):
                            df_length = len(df)
                            df.loc[df_length] = d
            except requests.exceptions.ConnectionError:
                r.status_code = "Connection refused"
        
        self.df = df
        return df
                
    def find_article(self, url):
        response = requests.get(url, verify=False)
        html = response.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        raw = soup.select(self.text_selector)[0]
        if raw.find('strong') is not None:
            unwanted = raw.find('strong')
            unwanted.extract()

        self.text = raw.text.strip()
        self.article = self.clean_text(self.text)
        return self.article
    
    def clean_text(self, text):
        cleaned_text = re.sub('[a-zA-Z]', '', text)
        cleaned_text = re.sub('[?!]', ' . ', cleaned_text)
        cleaned_text = re.sub('[\{\}\[\]\/,;:|\)*~`^·\-_+<>▶▽△▲⊙♡◀◆◈※◇■●━◎○@\#$%&\\\=\(\'\"ⓒ(\n)(\t)‘’“”〃]', ' ', cleaned_text)
        cleaned_text = re.sub('㎢㈜', ' ', cleaned_text)
        cleaned_text = cleaned_text.replace("🇲\u200b🇮\u200b🇱\u200b🇱\u200b🇮\u200b🇪\u200b", "")
        cleaned_text = cleaned_text.replace("한국경제TV, 무단 전재 및 재배포 금지", "")
        cleaned_text = cleaned_text.replace("이미지를 누르면 크게 볼 수 있습니다", "")
        output = ' '.join(cleaned_text.split())
        return output
    
    def save_func(self):
        dt = datetime.datetime.now()
        date = dt.strftime('%Y_%m_%d_%H%M%S')
        self.df.to_csv('../_data/' + '[' + self.agent + ']' + date + '[' + self.keyword + ']'\
                  + '.csv')
        
    def show_data(self):
        print(self.df.head())


# %%
#한겨레 검색 클래스
class Hani_search(Main_search):
    def __init__(self, keyword, page):
        super(Hani_search, self).__init__(keyword, page)
        self.agent = '한겨레'
        self.url = 'http://search.hani.co.kr/Search?command=query&media=news&sort=s&period=year&'
        self.parameter = {
                    'keyword': keyword,
                    'pageseq': page
                    }
        self.title_selector = 'ul.search-result-list li dt a'
        self.text_selector = 'div.article-text div.text'
        self.banned_list = ['인사', '알림', '[', '그림판', '소식']
        
    def search(self):
        super(Hani_search, self).search()


# %%
#중앙일보 검색 클래스
class Joins_search(Main_search):
    def __init__(self, keyword, page):
        super(Joins_search, self).__init__(keyword, page)
        self.agent = '중앙'
        self.url = 'http://news.joins.com/Search/TotalNews?'
        self.parameter = {
                'keyword': keyword,
                'Page': page,
                'StartSearchDate': '2020.01.01',
                'SortType' : 'Accuracy',
                'SearchCategoryType': 'JoongangNews'
                }
        self.title_selector = 'ul.list_default li h2 a'
        self.text_selector = 'div.article_body'
        self.banned_list = ['[',']']
    def search(self):
        super(Joins_search, self).search()


# %%
#한경 검색 클래스
class Hnky_search(Main_search):
    def __init__(self, keyword, page):
        super(Hnky_search, self).__init__(keyword, page)
        self.whitelist = 'www.hankyung.com/'
        self.agent = '한경'
        self.url = 'http://search.hankyung.com/apps.frm/search.news?&sort=RANK%2FDESC%2CDATE%2FDESC&'
        self.parameter = {
                'query': keyword,
                'page': page,
                'period': 'YEAR'
                }
        self.title_selector = 'div.txt_wrap > a'
        self.text_selector = '#articletxt'
        self.banned_list = ['의 국감', '신설법인', '종합']
    def search(self):
        super(Hnky_search, self).search()


# %%
def main_func(agent, keyword, pages, tf):
    
    if agent == '한겨레':
        func = Hani_search(keyword, pages)
    elif agent == '중앙':
        func = Joins_search(keyword, pages)
    elif agent == '한경':
        func = Hnky_search(keyword, pages)
    else:
        print('다시 입력해줘~')
        
    df = func.search() 
    func.save_func() if tf else tf
    print('작업 완료했어~')



# %%
if __name__ == '__main__':
    agent = input('[!] 언론사 입력 : ')
    keyword = input('[!] 검색어 입력 : ')
    pages = input('[!] 검색 페이지 수 : ')
    save_tf = '[!] csv로 저장할래? : '
    tf = query_yes_no(save_tf)
    main_func(agent, keyword, pages, tf)
    

# %%
