from flask import Flask
from flask import render_template
from flask import request

import networkx as nx
from pyvis.network import Network
import pandas as pd
import os

import matplotlib
#Library not loaded: @rpath/libwebp.7.dylib:
#--solution:https://github.com/conda-forge/opencv-feedstock/issues/219

matplotlib.rcParams['font.sans-serif']=['Taipei Sans TC Beta']
#from matplotlib.font_manager import _rebuild
#_rebuild()


#filter df & output html
def filter_func(data,parms):
    if parms==None: return data
    else : return data[data['Brand']==parms]
def draw_Graph_func(data):
    G = nx.from_pandas_edgelist(data,
        'Product_Name','cus_seg',edge_attr = 'title',create_using = nx.DiGraph())
    nt = Network('600px','50%',directed=True,heading = '知識圖譜')
    nt.from_nx(G)
    #nt.show_buttons(filter_ = ['physics'])
    nt.show(os.getcwd()+'/templates/Knowledge Graph.html')

pd_sim = pd.read_csv(os.getcwd()+"/vis_/product_sim.csv")

from Graph_HTML_edit import HTML_edit_func

app = Flask(__name__)
@app.route('/')
def render_func():
    #Get Brand Key
    for key in ['Brand']:
        #--渲染Brand--#
        try : #如果有篩選
            arg = request.args.get(key)
            df_tmp = filter_func(pd_sim,arg)
            draw_Graph_func(df_tmp)
            #生完html, 硬塞button
            HTML_edit_func()

        except: #如果沒有篩選 -> init
            draw_Graph_func(pd_sim)
            #生完html, 硬塞button
            HTML_edit_func()
    return render_template('Knowledge Graph.html')

if __name__ == '__main__':
    app.debug = True
    app.run()


