import random
import math
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from io import BytesIO

matplotlib.use('Agg')


# Define the symbol
x = sp.Symbol('x')

# Function to generate a random coefficient
def rand_coeff(min_val=-5, max_val=5, exclude_zero=False):
    val = 0
    while val == 0 if exclude_zero else False:
        val = random.randint(min_val, max_val)
    return val if not exclude_zero else val

# Function to randomly select a form and return the corresponding expression
def random_expr():
    form = random.choice([
        "poly", "poly_shifted", "exp", "log", "sin", "cos", "tan"
    ])
    a = rand_coeff(-10, 10, exclude_zero=True)
    b = rand_coeff(-10, 10, exclude_zero=True)

    if form == "poly":
        return a * x**b
    elif form == "poly_shifted":
        c = rand_coeff(-10, 10, exclude_zero=True)
        return (a * x + b)**c
    elif form == "exp":
        return a * sp.exp(b * x)
    elif form == "log":
        return a * sp.log(b * x)
    elif form == "sin":
        return a * sp.sin(b * x)
    elif form == "cos":
        return a * sp.cos(b * x)
    elif form == "tan":
        return a * sp.tan(b * x)

# Function to combine two expressions with a random operation
def generate_expression_latex():
    u = random_expr()
    v = random_expr()
    op = random.choice(['+', '-', '*', '/'])

    if op == '+':
        expr = u + v
    elif op == '-':
        expr = u - v
    elif op == '*':
        expr = u * v
    elif op == '/':
        expr = u / v

    return sp.latex(expr), sp.latex(sp.diff(expr, x))

def generate_polynomial():
    # Randomly generate coefficients a, b, c
    a = random.randint(-5, 5)
    while a == 0:  # ensure it's a quadratic
        a = random.randint(-5, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    # Create the polynomial using sympy for LaTeX representation
    x = sp.Symbol('x')
    poly_expr = a * x**2 + b * x + c
    return poly_expr
    
def get_polynomial_questions(f):
    # Question a: Intercepts
    x_intercepts = sp.solve(f, x)
    y_intercept = f.subs(x, 0)

    # Question b: Derivative and evaluation
    f_prime = sp.diff(f, x)
    x_val_for_derivative = random.randint(-5, 5)
    f_prime_at_val = f_prime.subs(x, x_val_for_derivative)

    # Question c: Area under the curve
    if len(x_intercepts) == 2 and all(sp.im(xi) == 0 for xi in x_intercepts):
        lower, upper = sorted([float(xi) for xi in x_intercepts])
    else:
        lower, upper = sorted([random.randint(0, 5), random.randint(6, 10)])

    area_under_curve = sp.integrate(f, (x, lower, upper))

    # Question d: Stationary points
    stationary_x_vals = sp.solve(f_prime, x)
    stationary_points = [(xi, f.subs(x, xi)) for xi in stationary_x_vals]

    # --- Solutions stored in variables ---
    function_expr = f
    latex_expr = sp.latex(f)
    x_intercepts_solution = x_intercepts
    y_intercept_solution = y_intercept
    derivative_expr = f_prime
    derivative_at_value = (x_val_for_derivative, f_prime_at_val)
    area_bounds = (lower, upper)
    area_solution = area_under_curve
    stationary_points_solution = stationary_points



def generate_polynomial_plot(poly_expr) -> BytesIO:
    latex_poly = sp.latex(poly_expr)
    f = sp.lambdify(x, poly_expr, modules='numpy')

    # Generate x values and corresponding y values
    x_vals = np.linspace(-5, 5, 400)
    y_vals = f(x_vals)

    # Plotting the function
    fig = plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=f"${latex_poly}$", color='blue')
    plt.title(r"$f(x) = " + latex_poly + r"$", fontsize=16)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)

    img = BytesIO()
    fig.savefig(img, format='png')
    plt.close(fig)  # Close the figure to free memory
    img.seek(0)    # Rewind the buffer to the beginning    

    return img