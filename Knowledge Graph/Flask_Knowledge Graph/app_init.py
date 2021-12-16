from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/') #init localhost: http://127.0.0.1:5000/
def render_func():

    #抓變動
    #call draw funtion-> new html
    return render_template('Knowledge Graph_init.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

