from flask import Flask,render_template,request,make_response,url_for,redirect,abort
import json,os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    
    category = db.relationship('Category',backref=db.backref('files',lazy='dynamic'))


    def __init__(self,title,category,content,create_time=None):
        self.title = title
        # self.category_id = category_id
        self.category = category
        self.content = content
        if create_time is None:
            self.create_time = datetime.now()
    def __repr__(self):
        return '<File id: {:d} name:{}>'.format(self.name)
    


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))


    def __init__(self,name):
        self.name =name

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    

@app.route('/')
def index():
    return render_template('index.html',artical_list = db.session.query(File).all())

@app.route('/files/<fileid>')
def file(fileid):
    file = db.session.query(File).filter(File.id==fileid).first()
    if file is None:
        abort(404)
    category = db.session.query(Category).filter(Category.id==file.category_id).first()
    return render_template('file.html',file=file,category=category.name)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',message='shiyanlou 404'),404

def init_data():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java',java,'File Content - Java is cool!')
    file2 = File('Hello Python',python,'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

if __name__=='__main__':
    pass
    # init_data()
