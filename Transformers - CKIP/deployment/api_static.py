from xml.dom.minidom import Element
from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

with open(r'./data/deployment/res_dict_w2v.pickle','rb') as f:
    data = pickle.load(f)

#根目錄
@app.route("/",methods=['GET','POST'])
def init():
    return 'Hello World!'

#annotation: 標記(告訴他有這個路徑，但不是要執行程式)
@app.route("/tag_query",methods=['GET','POST'])
def result():
    brand = request.values.get('brand')
    return jsonify({f"{brand}":data[brand]})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6666)