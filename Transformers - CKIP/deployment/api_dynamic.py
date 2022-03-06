from flask import Flask, jsonify, request
import pickle
import pandas as pd
import numpy as np
import os
import gensim #3.8.3
from gensim.models import KeyedVectors
from collections import deque
from itertools import compress
#Add custimize function
import sys
sys.path.append('./src')
from tagging import tagging, tagging_change_n_freq
from w2v_search import w2v_filtered_func



#---Init Loading---#
# gensim_model = KeyedVectors.load_word2vec_format('./model/w2v_CNA_ASBC_300d.vec' ,binary=False, encoding='utf-8', unicode_errors='ignore')

# del_set = []
# #load eyemining_file
# with open('./docs/eyemining_words.txt','r',encoding='utf-8') as f:
#     for line in f: del_set.append(line)
# #load stopword_file
# with open('./docs/stop_words.txt','r',encoding='utf-8') as f:
#     for line in f: del_set.append(line)

# del_set = set([x[:-1] for x in del_set])



#---FLASK---#
app = Flask(__name__)

#根目錄
@app.route("/",methods=['GET','POST'])
def init():
    return 'Hello World!'

#Predict
<<<<<<< Updated upstream
@app.route("/pred",methods=['GET','POST'])
def transformer_predict():
    brand = request.values.get('brand')
    element = request.values.get('element')

    #eval一個input list
    tmp_obj = tagging(brand,eval(element))
    tmp_obj = w2v_filtered_func(tmp_obj,gensim_model,del_set,4,0.1)
    return jsonify({tmp_obj.name:tmp_obj.tagging_list_w2v})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6666)
=======
# @app.route("/pred",methods=['GET','POST'])
# def transformer_predict():
#     req_dict = request.get_json()
#     brand = req_dict.get(brand,None)
#     element = req_dict.get(element,None)
    
#     #eval一個input list
#     tmp_obj = tagging(brand,eval(element))
#     tmp_obj = w2v_filtered_func(tmp_obj,gensim_model,del_set,4,0.1)
#     return jsonify({tmp_obj.name:tmp_obj.tagging_list_w2v})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000)
>>>>>>> Stashed changes
