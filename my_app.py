from flask import Flask, render_template_string, send_file, request
import question_generator
import uuid
import sympy as sp


app = Flask(__name__)

@app.route("/")
def home():
    return "<title>Home Page</title><h1>HOME PAGE</h1>"

@app.route("/hello-world")
def hello():
    return "hello world!"

query_lookup = {}

@app.route('/question_fancy')
def index():
    expr, sol = question_generator.generate_expression_latex() #r"E = mc^2"
    query_uuid = uuid.uuid4()
    page = {}
    quadratic = question_generator.generate_polynomial()
    page["question-2-polynomial"] = quadratic

    query_lookup[query_uuid] = page

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Maths</title>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
        </script>
    </head>
    <body>
        <h1>Questions</h1>
        <h3>Question 1</h3>
        <p>Find the derivative of \\({{ math }}\\)</p>
        <p>The answer is \\({{ sol }}\\)</p>
        <h3>Question 2</h3>
        <p>Look at this graph of the plot \\({{ quadratic }}\\)</p>
        <img src="../plot.png?{{ uuid }}">
    </body>
    </html>
    '''
    return render_template_string(html, math=expr, sol=sol, uuid=query_uuid, quadratic=sp.latex(quadratic))


@app.route('/plot.png')
def plot_png():
    query = uuid.UUID(request.query_string.decode())

    try:
        page = query_lookup[query]

        img = question_generator.generate_polynomial_plot(page["question-2-polynomial"])
        return send_file(img, mimetype="image/png")
    except KeyError:
        print("page not found")
        return ""
    

@app.route("/question")
def make_question():
    q = question_generator.generate_quadratic()
    return f"Question: {q.question}, Solution: {q.solution}"

if __name__ == '__main__':
    app.run(debug=True)
