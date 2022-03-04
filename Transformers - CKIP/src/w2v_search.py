from collections import deque
from itertools import compress
import numpy as np

#iput pickle file , return filted list
def w2v_filtered_func(pkl_obj, gensim_vec, del_set, top_n, keep_threshold):
    '''
    pkl_obj: brand實體物件(pickle)
    gensim_vec: 詞向量(vec)
    del_set: 贅字集合(set)
    top_n: 每個詞取與之simularity前n大的詞, 做累加計算
    keep_threshold: 保留累加quantile數列中, 大於keep_threshold的詞
    '''
    #不在贅字典的才計算
    l = [x[0] for x in pkl_obj.freq_list if x[0] not in del_set]
    #有可能清完有些是空的list: 直接return
    if l == []: 
        pkl_obj.tagging_list_w2v = []
        return pkl_obj
    tmp_l = deque(l); s = set()
    tmp_sim = np.zeros(len(l)) #紀錄投票分數
    
    #例外處理:如果我想取前幾大的比原本的Attribute長, 就只用原本的Attribute長度
    if top_n>len(l):
        top_n=len(l)

    while tmp_l:        
        tmp = tmp_l.popleft()
#        print(f"/*--當前變數:{tmp}--*/")
#        print(f"--各simularity的名字:--\n {l}")
#        print(f"--紀錄simularity的array:--\n {tmp_sim}")

        if tmp not in s :
            s.add(tmp)
        else: break

        dic = {}
        for x in tmp_l :
            #計算相似度, 記錄在dictionary裡
            try:
                dic[x] = gensim_vec.similarity(tmp,x)
            except:
                continue

        #找出前幾大的        
        sorted_list = sorted(dic.items(), key=lambda value: value[1], reverse=True)[:top_n]
#        print(f"標籤:{tmp} / 最相關的:{sorted_list}")

        #把前幾大的, 紀錄在array裡
        for item in sorted_list:
            tmp_sim[l.index(item[0])]+=item[1]

        #最後貼回去
#        print(f'----{tmp}結束----\n')
        tmp_l.append(tmp)
    
    pkl_obj.tagging_list_w2v = list(set(compress(l, tmp_sim>np.quantile(tmp_sim,keep_threshold))))
    return pkl_obj