from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json, urllib.request

with open('templates/config.json', 'r') as c:
    config = json.load(c)
    params = config["params"]
    

local_server = True

app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    phone_num = db.Column(db.String(12), nullable = False)
    msg = db.Column(db.String(120), nullable = False)
    date = db.Column(db.String(12), nullable = True)
    email = db.Column(db.String(20), nullable = False)
    


@app.route("/")
def home():
    return render_template('index.html', params = params)

@app.route("/home")
def homey():
    return render_template('home.html', params = params)

@app.route("/about")
def about():
    return render_template('about.html', params = params)

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        entry = Contacts(name = name, phone_num = phone, msg = message, date = datetime.now(), email = email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params = params)

@app.route("/test")
def test():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    
    return render_template ("index.html", params = params, name = dict['title'])




app.run(debug=True)

