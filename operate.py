from flask import Flask, render_template,session,request,redirect
import requests
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import date
import time
from sqlalchemy import text
from authlib.integrations.flask_client import OAuth
from termcolor import colored
import json
import pymysql
pymysql.install_as_MySQLdb()


with open("config.json",'r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/imagerender'
db = SQLAlchemy(app)

class Regulation_table(db.Model):
    dateTime = db.Column(db.String(100))
    SNo = db.Column(db.Integer,primary_key=True)



app.config['UPLOAD_FOLDER']=params['upload_location']
app.config['SECRET_KEY'] = 'secret message'
oauth = OAuth(app)

# Google Id and Secret Key

GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

@app.route('/')
def beforeLogin():
    session['Permission']='Denied'
    return render_template("login.html")

@app.route('/login')
def login():
    if request.args.get("next"):
        session["next"]=request.args.get("next")

    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&response_type=code&redirect_uri=http://127.0.0.1:5000/home&client_id={GOOGLE_CLIENT_ID}")


@app.route('/home')
def home():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
        "redirect_uri": "http://127.0.0.1:5000/home"
    })
    v=r.json()
    if "access_token" in v.keys() or session.get("Permission")=="Access":
        session['Permission']='Access'
        return render_template("home.html")
    else:
        session['Permission']='Denied'
        return "<center><h4>Invalid Request</h4></center>"

@app.route('/upload_image',methods=['GET', 'POST'])
def upload_image():
    
    sql = text('SELECT * FROM regulation_table ORDER BY dateTime DESC LIMIT 6')
    result1 = db.engine.execute(sql)
    later = datetime.now()
    result2=[result[0] for result in result1]
    counter=0
    for i in result2:
        diff = (later-i)
        print("diff.days*24*60*60 + diff.seconds",diff.days*24*60*60 + diff.seconds)
        if (diff.days*24*60*60 + diff.seconds)<60:
            counter+=1
        else:
            counter=0
            break
    print("Counter",counter)

    if (counter<=4):
        if (request.method=="POST"):

            # Insert Data
            entry=Regulation_table(dateTime=datetime.now())
            db.session.add(entry)
            db.session.commit()

            f=request.files['imageData']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return render_template("upload_image.html",result = "static/img/"+f.filename)
                
        else:
            return "<center><h4>Invalid Request</h4></center>"
        
    else:
        message="Too many Access,Please wait for"+(60-(diff.days*24*60*60 + diff.seconds))
        return "<center><h4>"+message+"</h4></center>"




app.run(debug=True)


