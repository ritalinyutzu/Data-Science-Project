import requests
import re
import warnings
import os
from conda  import InsecureRequestWarning
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle

# 忽略不安全連線警告
warnings.simplefilter('ignore', InsecureRequestWarning)

class momo_hashtag:
    def __init__(self,goods_code):
        self.goods_code = goods_code
        self.url = f'https://m.momoshop.com.tw/goods.momo?i_code={str(self.goods_code)}'
        self.headers = {'cookie':'isTN1=1; loginRsult=1;',
            'content-type': 'text/html; charset = UTF-8', 
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        self.request_func()
    
    def request_func(self):
        try:
            res = requests.get(self.url,verify=False,headers=self.headers)
            if res.status_code == 200:        
                soup = BeautifulSoup(res.text, 'html.parser')

                #name
                self.name = soup.find('article', {'class':'keywordsBlock'}).find('ul').get('goodsname')

                #hashtag
                hashtag = [];
                for keywords in soup.find('article', {'class':'keywordsBlock'}).find_all('li'):
                    if keywords.get('attrname') is not None:
                        hashtag.append(keywords.get('attrname') + '-' + keywords.get('attrcontentname'))    
                self.hashtag = hashtag
            else:
                print(f"status_code:{res.status_code}")
                
        except:
            print(f'No name->goods_code:{self.goods_code}')
    
    def result_func(self):
        return self.goods_code , self.hashtag
    
def main():
    os.chdir(r'..') # goods_code_file
    data = pd.read_csv('./goods_info.txt')
    
    goodscode_res = []
    keyword_res = []
    fail_res = []

    for x in data['GOODS_CODE']:
        try:
            tmp_goods_code , tmp_keywords = momo_hashtag(x).result_func()
            goodscode_res.append(tmp_goods_code)
            keyword_res.append(tmp_keywords)
            time.sleep(20)
        except:
            fail_res.append(x)
            print(f'Fail:{x}')

    res_df = pd.DataFrame({'goodscode_res':goodscode_res,
                           'keyword_res':keyword_res})
    
    #write result
    with open('./res_df.pickle','wb') as f:
        pickle.dump(res_df,f)

    with open('./fail_res.pickle','wb') as f:
        pickle.dump(fail_res,f)

if __name__ == '__main__':
    main()