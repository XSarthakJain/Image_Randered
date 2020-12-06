from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload_image')
def upload_image():
    return render_template("upload_image.html")

app.run(debug=True)
