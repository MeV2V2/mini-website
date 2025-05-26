from flask import Flask, render_template_string, send_file, request, Response
import question_generator
import multiple_choice
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
   
    mcq = multiple_choice.questions_html(10)
 
    query_lookup[query_uuid] = page

    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head> 
        <link rel="stylesheet" href="style.css">

        <style>
            .MathJax {{
                pointer-events: none; /* disables click, hover, etc. */
                user-select: none;    /* prevents selection */
            }}
        </style>

        <!-- MathJax with custom config to disable menu -->
        <script>
            window.MathJax = {{
                options: {{
                    renderActions: {{
                        addMenu: []
                    }}
                }}
            }};
        </script>

        <meta charset="UTF-8">
        <title>Maths</title>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
        </script>
    </head>
    <body>
        <h1>Multiple Choice Questions</h1>
        {mcq}

        <h1>Short Answer Questions</h1>
        <h3>Question 1</h3>
        <p>Find the derivative of \\({ expr }\\)</p>
        <p>The answer is \\({ sol }\\)</p>
        <h3>Question 2</h3>
        <p>Look at this graph of the plot \\({ sp.latex(quadratic) }\\)</p>
        <img src="../plot.png?{ query_uuid }">
    </body>
    </html>
    '''
    return html


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

@app.route("/style.css")
def create_style():
    css = """
        <style>
        body {
            font-family: "Georgia", serif;
            background-color: #f9f9f9;
            color: #222;
            margin: 40px auto;
            max-width: 800px;
            line-height: 1.6;
        }

        p {
            margin-bottom: 10px;
        }

        b {
            font-size: 1.1em;
        }

        .question-container {
            background-color: #fff;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .question-container label {
            display: block;
            margin: 8px 0;
            padding: 6px 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        .question-container label:hover {
            background-color: #f0f0f0;
        }

        input[type="radio"] {
            margin-right: 8px;
            transform: scale(1.1);
        }

        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 40px;
            font-weight: normal;
        }

        button {
            display: block;
            margin: 40px auto;
            padding: 12px 24px;
            font-size: 1em;
            font-family: inherit;
            background-color: #4b6cb7;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        button:hover {
            background-color: #3a58a0;
        }
        </style>"""
    
    return Response(css, mimetype='text/css')

if __name__ == '__main__':
    app.run(debug=True)
