import pandas as pd
import numpy as np
import pickle
import os

#Add custimize function
import sys
sys.path.append('./src')
from tagging import tagging, tagging_change_n_freq


def main():
    #--input data--#
    with open(f'./data/crawler_res/pickle/input_20220225.pickle','rb') as f:
        df = pickle.load(f).reset_index(drop=True)

    if not os.path.exists('./data/tagging_res'):
        os.makedirs('./data/tagging_res')

    #--Tagging--#
    success_list = []; res_dict = {}
    for i, x in enumerate(df.values):
        try:
            globals()[f"x{i}"] = tagging(x[0],x[1])
            res_dict[eval(f"x{i}").name] = eval(f"x{i}").tagging_list
            with open(f'./data/tagging_res/x{i}.pickle','wb') as f:
                pickle.dump(eval(f"x{i}"),f)            
        except:
            print(f'Fail: x{i}')
    
    #--為了部署查詢方便: save dict for query--#
    with open(f'./data/deployment/res_dict.pickle','wb') as f:
        pickle.dump(res_dict,f)

if __name__=='__main__':
    main()