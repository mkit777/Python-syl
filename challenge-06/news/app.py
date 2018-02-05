from flask import Flask,render_template,request,make_response,url_for,redirect,abort
import json
import os
app = Flask(__name__)

@app.route('/')
def index():
    path='/home/shiyanlou/files/'
    artical_list=[]
    for filename in os.listdir(path):
        if filename.split('.')[1] == 'json':
            with open(path+filename) as file:
                j=json.loads(file.read())
                j['filename']=filename.split('.')[0]
                artical_list.append(j)

    assert len(artical_list)==2,'json file load error'
    return render_template('index.html',artical_list=artical_list)

@app.route('/files/<filename>')
def file(filename):
    path = '/home/shiyanlou/files/'+filename+'.json'
    if not  os.path.exists(path):
        abort(404)
    with open(path) as file:
        artical = json.loads(file.read())
    return render_template('file.html',artical=artical)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',message='shiyanlou 404'),404


if __name__=='__main__':
    app.run()
