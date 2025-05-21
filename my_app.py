from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>HOME PAGE</h1>"

@app.route("/hello-world")
def hello():
    return "hello world!"


if __name__ == '__main__':
    app.run(debug=True)