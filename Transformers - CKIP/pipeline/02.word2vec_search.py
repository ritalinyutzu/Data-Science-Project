import pandas as pd
import numpy as np
import pickle
import os
import gensim #3.7.0
from gensim.models import KeyedVectors
from collections import deque
from itertools import compress
#Add custimize function
import sys
sys.path.append('./src')
from tagging import tagging, tagging_change_n_freq
from w2v_search import w2v_filtered_func

def main():
    #----------------------------------#
    #---load file path + pickle file---#
    load_pkl_path = './data/tagging_res'
    max_num = max([int(x.split('.')[0][1:]) for x in os.listdir(load_pkl_path) if 'pickle' in x ])
    def read_brand_pkl(i):
        try:
            with open(load_pkl_path + f'/x{i}.pickle', 'rb') as f:
                globals()[f'x{i}'] = pickle.load(f)
            return f'x{i}'
        except: 
            print(f'Fail: x{i}')

    success_list=[]
    for i in range(max_num+1):
        success_list.append(read_brand_pkl(i))
        
    success_list = [x for x in success_list if x != None]


    #----------------------------------#
    #---gensim model 3.7.0---#
    #M054111023/nsysuMBA
    #Some method: 
    #   model.wv.vocab(str): 查哪些單詞在裡面
    #   model.most_similar(str): 最相關的詞是哪些
    model = KeyedVectors.load_word2vec_format('./model/w2v_CNA_ASBC_300d.vec' ,binary=False, encoding='utf-8', unicode_errors='ignore')

    del_set = []
    #load eyemining_file
    with open('./docs/eyemining_words.txt','r',encoding='utf-8') as f:
        for line in f: del_set.append(line)
    #load stopword_file
    with open('./docs/stop_words.txt','r',encoding='utf-8') as f:
        for line in f: del_set.append(line)

    del_set = set([x[:-1] for x in del_set])


    #----------------------------------#
    res_dict={}
    for x in success_list:
        try:
            globals()[f'{x}'] = w2v_filtered_func(eval(x),model,del_set,4,0.1)
            res_dict[eval(f"{x}").name] = eval(f"{x}").tagging_list_w2v
        except: 
            print(f'Fail:{x}')

    with open(f'./data/deployment/res_dict_w2v.pickle','wb') as f:
        pickle.dump(res_dict,f)

if __name__=='__main__':
    main()    



