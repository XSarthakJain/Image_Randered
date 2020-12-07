from flask import Flask, render_template,session,request,redirect
import requests
# from .models import User
import os
#import secrets
# from flask.ext.sqlalchemy import SQLAlchemy
import os
# from flask import Flask, flash, request, redirect, url_for
#from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from termcolor import colored


# UPLOAD_FOLDER = '/static/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)  
app.config['SECRET_KEY'] = 'oh_so_secret'
oauth = OAuth(app)
# GOOGLE_CLIENT_ID=""
# GOOGLE_CLIENT_SECRET=""



# oauth.register(
#     name='google',
#     client_id="",
#     client_secret="",
#     access_token_url="",
#     access_token_params=None,
#     authorize_url="",
#     autherize_params=None,
#     api_base_url="",

#     # ...
#     # server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid profile email'}
# )



# @app.route('/login')
# def login():
#     redirect_uri = url_for('authorize', _external=True)
#     return oauth.twitter.authorize_redirect(redirect_uri)

# @app.route('/authorize')
# def authorize():
#     token = oauth.twitter.authorize_access_token()
#     resp = oauth.twitter.get('account/verify_credentials.json')
#     profile = resp.json()
#     # do something with the token and profile
#     return redirect('/')


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/uploadImageProcess', methods=['GET', 'POST'])
# def upload_file():
    # if request.method == 'GET':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))
    #return render_template("upload_image.html")

# @app.route("/access_token", methods=["POST"])
# def access_token():
#     # _app = c.execute("SELECT * FROM apps WHERE client_id=:id AND client_secret=:sec", {"id": request.form.get("client_id"), "sec": request.form.get("client_secret")}).fetchall()

#     # code = c.execute("SELECT * FROM oauth_codes WHERE code=:c", {"c": request.form.get("code")}).fetchall()
#     if len(code) == 0:
#         return "INVALID CODE"

#     if len(_app) == 0:
#         return "INVALID CLIENT ID/CLIENT SECRET!"

#     while True:
#         token = random_str(70)
#         _ = c.execute("SELECT * FROM tokens WHERE token=:t", {"t": token}).fetchall()
#         if len(_) == 0:
#             break
#     c.execute("DELETE FROM oauth_codes WHERE code=:code", {"code": request.form.get("code")})
#     conn.commit()

#     c.execute("INSERT INTO tokens (app_id, user_id, token) VALUES (:a, :u, :t)", {"a": _app[0][0], "u": code[0][1], "t": token}).fetchall()
#     conn.commit()

#     return token




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
    print("Color",r.json())

    
    # r = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={r.json()["access_token"]}').json()
    # #user = c.execute("SELECT * FROM users WHERE user_id=:user_id", {"user_id": r["id"]}).fetchall()
    # if len(user) != 0:
    #     session["user_id"] = user[0][0]
    #     session["name"] = user[0][1]
    #     session["avatar"] = user[0][2]
    # else:
    #     c.execute("INSERT INTO users (user_id, name, photo) VALUES (:id, :name, :photo)", {"id": r["id"], "name": r["name"], "photo": r["picture"]})
    #     conn.commit()
    #     session["user_id"] = r["id"]
    #     session["name"] = r["name"]
    #     session["avatar"] = r["picture"]

    # if session.get("next"):
    #     return redirect(session.get("next"))
    v=r.json()
    print(type(v))
    if "access_token" in v.keys() or session.get("Permission")=="Access":
        session['Permission']='Access'
        return render_template("home.html")
    else:
        session['Permission']='Denied'
        return "Invalid Request"
    #return render_template("home.html")
# @app.route('/uploadImageProcess',method=['GET'])
# def uploadImageProcess():
#     target=os.path.join(APP_ROOT,'images/')
#     print(target)
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     else:
#         print("Couldn't create upload directory : {}".format(target))
#     print(request.files.getlist("file"))

#     for upload in request.files.getlist("file"):
#         print("upload")
#         print("{} is the fileName".format(upload.filename))
#         filename=upload.filename
#         destination="/".join([target,"temp.jpg"])
#         upload.save(destination)

#     return "uploadImageProcess"

@app.route('/upload_image')
def upload_image():
    return render_template("upload_image.html")



app.run(debug=True)


