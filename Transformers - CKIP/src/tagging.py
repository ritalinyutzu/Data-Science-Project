import re
import pickle
from opencc import OpenCC
cc = OpenCC('s2tw')

with open('./model/ws_driver.pickle','rb') as f :
    ws_driver = pickle.load(f)
with open('./model/pos_driver.pickle','rb') as f :
    pos_driver = pickle.load(f)
with open('./model/ner_driver.pickle','rb') as f :
    ner_driver = pickle.load(f)

class tagging:
    def __init__(self,name,data):
        self.name = name; self.data = data
        self.Regex_func(); self.NER_func(); self.WsPos_func()
        self.MainProcess_WordFreq()

    #--先把爬到的資料清乾淨
    def Regex_func(self):
        t = []
        for l in self.data: 
            #清掉爬蟲日期 & s2tw
            l = cc.convert(re.sub(r"[(A-Za-z) (0-9), (0-9) —|(0-9)年(0-9)月(0-9)日]+",'',l))
            #append結果
            t.append(re.sub(r"[^\u4e00-\u9fa5|^(0-9)]+",' ',l) )
        self.data = t

    #--把原本資料中NER挑出來，並去除掉
    def NER_func(self):
        ner = ner_driver(self.data); ner_s = []
        for i in range(len(ner)):
            ner_s.extend(x.word for x in ner[i] if x.word not in ner_s)
        for i in range(len(self.data)):
            tmp_s = self.data[i]
        for x in ner_s:
            tmp_s = tmp_s.replace(x,"")
        self.data[i] = tmp_s 

    def WsPos_func(self):
        ws = ws_driver(self.data); pos = pos_driver(ws) #詞性  
        self.ws_res ,self.pos_res = self.pack_ws_pos_sentece(ws,pos)

    #input: list in list
    def pack_ws_pos_sentece(self,sentence_ws, sentence_pos): #要加self的原因是告訴這個class這個function有這兩個引數
        assert len(sentence_ws) == len(sentence_pos)
        res_ws = []; res_pos = [] 
        pos_set = set(['Na','Nb','Nc','VC','Vn']) #定義保留的詞性
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            # Two-Pointer
            l_idx = 0; r_idx=len(word_pos)-1
            while l_idx<=r_idx:
                if  word_pos[l_idx] in pos_set:
                    word_ws[l_idx] , word_ws[r_idx] =  word_ws[r_idx] , word_ws[l_idx]
                    word_pos[l_idx] , word_pos[r_idx] =  word_pos[r_idx] , word_pos[l_idx]
                    r_idx-=1
                else: l_idx+=1
            res_ws.append(word_ws[l_idx:])
            res_pos.append(word_pos[l_idx:])
        return res_ws , res_pos
  
    #--flattern list :遍歷所有文字, 留下討論度高的
    def MainProcess_WordFreq(self,n_freq=15):
        dic ={}
        for l in self.ws_res:
            for x in l:
                if x not in dic : dic[x]=1
                else : dic[x]+=1
        tmp =[]; tmp_name = []
        for x in dic.items():
        #清除空白 & 特店/特色等字串
            if re.match(r"[^ \s*|^特.|^品.|^理.|^精神.|^價值.|^故.|^形.|^名.]",x[0]):
                if x[1]>n_freq and len(x[0])>1:
                    tmp.append((x[0],x[1]))
                    tmp_name.append(x[0])
        self.tagging_list = tmp_name
        self.freq_list = tmp

def tagging_change_n_freq(pkl_obj,n):
    pkl_obj.MainProcess_WordFreq(n_freq=n)
    return pkl_obj

