import json
import requests
import time
import re
import os
import warnings
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup



""" 初始化 """
# 忽略不安全連線警告
warnings.simplefilter('ignore', InsecureRequestWarning)

# 使用header偽裝成edge瀏覽器下瀏覽行為
headers = {'content-type': 'text/html; charset = UTF-8', 
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'
          }


sleep_time = 5

def timer(func):
    def wrapper(*args, **kwargs):
        tic = time.time()
        value = func(*args, **kwargs)
        print('Time consumed: {} sec.'.format(time.time()-tic))
        return value
    return wrapper



class Merchant:
    def __init__(self, name, keyword, page):
        self.name = name
        self.page = page
        self.keyword = keyword
        self.get_html()
        self.parse_attr()
        
    
    def get_html(self):
        url = 'https://google.com/search?q={}+{}&start={}'.format(self.name, self.keyword, (self.page-1)*10)
        count = 0
        
        while count < 3:
            try:
                result = requests.get(url, verify=False, auth=('user', 'pass'), headers=headers)
                if result.status_code == 200:
                    self.html = result.text
                    break
                elif result.status_code == 429:
                    count = count+1
                    time.sleep(10*60)
            except:
                time.sleep(sleep_time)
                count = count+1
        else:
            raise ConnectionError('Cannot get the html')
    
    def parse_attr(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.soup = soup
        
        self.top_address = [element.text for element in soup.findAll('div', {'class':'sXLaOe'})]
        
        self.title_list = [element.find('h3').text for element in soup.findAll('div', {'class':'yuRUbf'})]
        self.summary_list = [element.text for element in soup.findAll('div', {'class':'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})]
        self.link_list = [element.find('a')['href'] for element in soup.findAll('div', {'class':'yuRUbf'})]
        self.presented_link_list = [element.text for element in soup.findAll('div', {'class':'TbwUpd NJjxre'})]
        self.featured_snippets_list = [element.text for element in soup.findAll('span', {'class':'hgKElc'})]
        
        self.service = [element.text.replace(u'\xa0', ' ') for element in soup.findAll('c-wiz', {'class':'u1M3kd W2lMue'})]
        self.product = [element.text for element in soup.findAll('div', {'class':'zPcHee'})]
        self.user_comment = [element.text for element in soup.findAll('a', {'class':'a-no-hover-decoration'})]
        
        self.address_and_phone_no = [element.text for element in soup.findAll('span', {'class':'LrzXr'})]
        self.phone_no = [element.text for element in soup.findAll('a', {'data-dtype':'d3ifr'})]
        self.map_desc = [element.text for element in soup.findAll('span', {'class':'YhemCb'})]
        self.map_suggested_list = [element.text for element in soup.findAll('div', {'class':'cXedhc'})]
        self.google_rating = [element.text for element in soup.findAll('span', {'class':'Aq14fc'})]
        self.google_map_name = [element.text for element in soup.findAll('h2', {'data-attrid':'title'})]
        
        self.related_search = [element.text for element in soup.findAll('div', {'class':'s75CSd OhScic AB4Wff'})]

    
    def to_dict(self, drop_html=True):
    
        result = {
                    'name' : self.name,
                    'top_address' : self.top_address,
                    'title_list' : self.title_list,
                    'summary_list' : self.summary_list,
                    'link_list' : self.link_list,
                    'presented_link_list' : self.presented_link_list,
                    'featured_snippets_list' : self.featured_snippets_list,
                    'service' : self.service,
                    'product' : self.product,
                    'user_comment' : self.user_comment,
                    'address_and_phone_no' : self.address_and_phone_no,
                    'phone_no' : self.phone_no,
                    'map_desc' : self.map_desc,
                    'map_suggested_list' : self.map_suggested_list,
                    'google_rating' : self.google_rating,
                    'google_map_name' : self.google_map_name,
                    'related_search' : self.related_search
                 }
        if not drop_html:
            result['html'] = self.html
        return result


def load_google_summary(keyword, pages):
    with open('./brands.txt', 'r', encoding='utf-8') as f:
        brands = f.readline().split('、')

    result_dict = dict()
    for brand in brands:
        result_dict[brand] = []

    for i in range(1,pages+1,1):
        with open(r'.\result_{}_{}.json'.format(keyword, i), 'r') as f:
            for brand in json.load(f):
                result_dict[brand['name']].append(brand['summary_list'])

    for brand in brands:
        summary_list = []
        for summary in result_dict[brand]:
            summary_list.extend(summary)
        result_dict[brand] = summary_list
    df = pd.DataFrame([result_dict]).T
    df.columns = ['summary_list']
    return df

# CHECK WHERE TO STORE BEFORE YOU RUN 
fp_output = r'/content/result_{}_{}.json'
fp_job_status = r'/content/job_status_{}_{}.json'

brands = ['Nike','The Body Shop']

pages = 5

# INPUT YOUR KEYWORDS
keywords = ['品牌 精神', '品牌 價值']
sleep_time = 5 #每一頁要隔五秒

start_time = time.time()
tic = time.time()
toc = time.time()

for i, keyword in enumerate(keywords):
    if i != 0:
        time.sleep(30) #大量的話要久一點
    for page in range(1,pages+1,1):

        result = list()
        job_status = {'fail_list' : [], 'success_list' : [], 'todo': brands, 'done_count': 0}

        for brand in job_status['todo']:
            
            if time.time()-tic < sleep_time:
                time.sleep(sleep_time)
                
            tic = time.time()
            
            try:
                result.append(Merchant(brand, keyword, page).to_dict())
                job_status['success_list'].append(brand)
                
            except:
                job_status['fail_list'].append(brand)
            job_status['done_count'] += 1

            if job_status['done_count'] % 100 == 0: 
                
                print('Jobs done: {}\nTime consumed: {:.1f}\nTotal time consumed: {:.1f}'.format(job_status['done_count'], time.time()-toc, time.time()-start_time))
                print('Success count: {} Fail count: {}'.format(len(job_status['success_list']), len(job_status['fail_list'])))
                print('===========================================================================')
                toc = time.time()

        with open(fp_output.format(keyword, page), 'w') as f:
            f.write(json.dumps(result))
        with open(fp_job_status.format(keyword, page), 'w') as f:
            json.dump(job_status, f)
            
        print('Keyword: {}, page: {} done.'.format(keyword, page))
        print('===========================================================================')