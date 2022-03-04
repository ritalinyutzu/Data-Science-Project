import json
import requests
import time
import re
import os
import warnings
import pickle
import pandas as pd
from bs4 import BeautifulSoup

""" 初始化 """
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 忽略不安全連線警告
#warnings.simplefilter('ignore', InsecureRequestWarning)

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

def scrape_google(brands, keywords, pages, output_dir, job_status_dir, sleep_time_per_q=5, sleep_time_per_keyword=1800):
    start_time = time.time()
    tic = time.time()
    toc = time.time()

    for i, keyword in enumerate(keywords):
        # 換關鍵字時暫停sleep_time_per_keyword以防被擋
        if i != 0:
            time.sleep(sleep_time_per_keyword)

        for page in range(1,pages+1,1):

            result = list()
            job_status = {'fail_list' : [], 'success_list' : [], 'todo': brands, 'done_count': 0}

            for brand in job_status['todo']:
                # 若搜尋時間小於sleep_time_per_q則睡sleep_time_per_q秒
                if time.time()-tic < sleep_time_per_q:
                    time.sleep(sleep_time_per_q)

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

            # 一頁存一次
            with open(os.path.join(output_dir, f'result_{keyword}_{page}.json'), 'w') as f:
                f.write(json.dumps(result))
            with open(os.path.join(job_status_dir, f'job_status_{keyword}_{page}.json'), 'w') as f:
                json.dump(job_status, f)

            print('Keyword: {}, page: {} done.'.format(keyword, page))
            print('===========================================================================')
    print('Done scrapping.')
    
def merge_result_by_keyword(brands, keyword, pages, output_dir):
 
    result_dict = dict()
    for brand in brands:
        result_dict[brand] = dict()
        result_dict[brand]['name'] = brand
        result_dict[brand]['summary_list'] = []
        result_dict[brand]['featured_snippets_list'] = []
        result_dict[brand]['link_list'] = []
        result_dict[brand]['presented_link_list'] = []
        # 會抓到廣告連結，需做例外處理
        result_dict[brand]['other_link'] = []
        result_dict[brand]['other_presented_link'] = []
        
    for i in range(1,pages+1,1):
        with open(os.path.join(output_dir, f'result_{keyword}_{i}.json'), 'r') as f:
            for brand in json.load(f):
                len_summary = len(brand['summary_list'])
                len_link = len(brand['link_list'])
                len_presented_link = len(brand['presented_link_list'])
                
                result_dict[brand['name']]['summary_list'].extend(brand['summary_list'])
                result_dict[brand['name']]['featured_snippets_list'].extend(brand['featured_snippets_list'])
                
                # 廣告連結例外處理
                if len_summary == len_link:
                    result_dict[brand['name']]['link_list'].extend(brand['link_list'])
                else: 
                    result_dict[brand['name']]['link_list'].extend(brand['link_list'][len_link-len_summary:])
                    result_dict[brand['name']]['other_link'].extend(brand['link_list'][0:len_link-len_summary])
                    
                if len_summary == len_presented_link:
                    result_dict[brand['name']]['presented_link_list'].extend(brand['presented_link_list'])
                else: 
                    result_dict[brand['name']]['presented_link_list'].extend(brand['presented_link_list'][len_presented_link-len_summary:])
                    result_dict[brand['name']]['other_presented_link'].extend(brand['presented_link_list'][0:len_presented_link-len_summary])

    
    result_list = []
    for key in result_dict.keys():
        result_list.append(result_dict[key])

    df = pd.DataFrame(result_list)

    return df

def save_as_pickle(brands, keyword_df_list, pickle_dir):
    result_dict = dict()
    for brand in brands:
        result_dict[brand] = dict()
        result_dict[brand]['name'] = brand
        result_dict[brand]['summary_list'] = []
    for df in keyword_df_list:
        for i, row in df.iterrows():
            result_dict[row['name']]['summary_list'].extend(row['summary_list'])
    df = pd.DataFrame(result_dict).T
    df.to_pickle(os.path.join(pickle_dir , f'input_{time.strftime("%Y%m%d", time.gmtime(time.time()))}.pickle'))

def get_summary_df(brands, keywords, pages):
    # Create directories if not exist
    output_dir = r'./data/crawler_res/raw/'
    job_status_dir = r'./data/crawler_res/job_status/'
    pickle_dir = r'./data/crawler_res/pickle/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(job_status_dir):
        os.makedirs(job_status_dir)
    if not os.path.exists(pickle_dir):
        os.makedirs(pickle_dir)
        
    # CONFIG SLEEPING TIME (5 sec per q is okay)
    # Sleep_time_per_keyword: 之前爬13xx個品牌時設1800沒遇到問題
    sleep_time_per_q = 5
    sleep_time_per_keyword = 10

    scrape_google(brands, keywords, pages, output_dir, job_status_dir, sleep_time_per_q, sleep_time_per_keyword)
    keyword_df_list = [merge_result_by_keyword(brands, keyword, pages, output_dir) for keyword in keywords]
    save_as_pickle(brands, keyword_df_list, pickle_dir)


def main():
    # INPUT YOUR BRANDS/PRODUCTS
    brands = ['TiMISA','琉璃工房','Levis','GUESS','SONY']
    # INPUT YOUR KEYWORDS
    pages = 5
    keywords = ['品牌 故事', '品牌 形象','品牌 精神']
    get_summary_df(brands, keywords, pages)

if __name__ == '__main__':
    main()