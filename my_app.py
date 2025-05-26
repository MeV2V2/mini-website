from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>HOME PAGE</h1>"

@app.route("/hello-world")
def hello():
    return "hello world!"

@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')