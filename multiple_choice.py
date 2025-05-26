import random
import question_generator
import sympy as sp
from math import comb

x = sp.symbols('x')

class MultipleChoice:
    # answers is a list of length 4, with the first being the correct answer
    def __init__(self, question: str, answers: list, question_type: str = ""):
        self.question = question
        self.correct_answer = answers[0]
        self.question_type = question_type
        
        random.shuffle(answers)
        self.a, self.b, self.c, self.d = answers


def generate_multiple_choice_0() -> MultipleChoice:
    a = random.randint(1, 5) 
    b = random.randint(1, 10) 
    c = random.randint(-5, 5) 

    y = sp.log(a * x + b) + c

    q = f"The asymptote(s) of the graph of \( {sp.latex(y)} \) are"
    answers = [
        f"\( x = {sp.Rational(-b,a)} \) only",
        f"\( x = {sp.Rational(b, a)} \) only",
        f"\( y = {c} \) only",
        f"\( x = {sp.Rational(-b, a)} \) and \( y = {c} \)"
    ]

    return MultipleChoice(q, answers)


def generate_multiple_choice_2() -> MultipleChoice:
    # Random values for derivative and initial condition
    a = random.randint(1, 4)
    b = random.randint(-5, 5)
    c = random.randint(0, 10)
    x0 = random.randint(0, 5)
    x1 = x0 + random.randint(1, 3)

    # Derivative and integration
    f_prime = a * x + b
    f = sp.integrate(f_prime, x) + sp.Symbol('C')
    C_value = sp.solve(f.subs(x, x0) - c, sp.Symbol('C'))[0]
    f_full = f.subs(sp.Symbol('C'), C_value)
    correct_value = f_full.subs(x, x1)

    # Generate unique incorrect options
    wrong_answers = set()
    while len(wrong_answers) < 3:
        perturb = random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        wrong = correct_value + perturb
        if wrong != correct_value:
            wrong_answers.add(wrong)

    # Assemble and shuffle answers
    answers = [f"\\( {correct_value} \\)"] + [f"\\( {val} \\)" for val in wrong_answers]
    random.shuffle(answers)

    # Question string
    q = (
        f"Let \( f'(x) = {sp.latex(f_prime)} \), and \( f({x0}) = {c} \). "
        f"What is the value of \( f({x1}) \)?"
    )

    return MultipleChoice(q, answers)

def generate_multiple_choice_3() -> MultipleChoice:
    k = sp.Symbol('k')
    num_values = 4

    # Start x at a random integer ≥ 1
    start_x = random.randint(1, 5)
    values = list(range(start_x, start_x + num_values))

    # Random coefficients for k
    coeffs = [random.randint(1, 5) for _ in range(num_values)]
    probs = [c * k for c in coeffs]

    # Solve for k
    total_eq = sp.Eq(sum(probs), 1)
    k_val = sp.solve(total_eq, k)[0]

    # Random threshold for P(X ≥ threshold)
    threshold_index = random.randint(1, num_values - 2)
    threshold_value = values[threshold_index]
    target_prob_expr = sum(probs[i] for i in range(threshold_index, num_values))
    target_prob = float(target_prob_expr.subs(k, k_val).evalf())
    correct_formatted = f"{target_prob:.3f}"

    # Generate distractors
    distractors = []
    offsets = [-0.1, 0.1, 0.2]
    for offset in offsets:
        candidate = max(0.0, min(1.0, round(target_prob + offset, 3)))
        if abs(candidate - target_prob) > 1e-4:
            distractors.append(f"\\( {candidate:.3f} \\)")

    # Fill to 4 choices
    all_answers = [f"\\( {correct_formatted} \\)"] + distractors
    while len(all_answers) < 4:
        rand_val = round(random.uniform(0.1, 0.9), 3)
        if abs(rand_val - target_prob) > 1e-4:
            all_answers.append(f"\\( {rand_val:.3f} \\)")
    random.shuffle(all_answers)

    # Build table string
    table_rows = "\n".join(f"{x} & {c}k \\\\" for x, c in zip(values, coeffs))
    q = (
        "A discrete random variable \( X \) has the following probability distribution:\n\n"
        "\\[ \\begin{array}{c|c}\n"
        "x & P(X = x) \\\\\n"
        "\\hline\n"
        f"{table_rows}\n"
        "\\end{array} \\]\n\n"
        f"What is the value of \( P(X \\geq {threshold_value}) \)?"
    )

    return MultipleChoice(q, all_answers)

# 4
def generate_multiple_choice_4() -> MultipleChoice:
    # 1. Generate Random Inputs
    a = random.randint(-10, 0)
    b = random.randint(a + 1, 10)
    c = random.randint(b + 1, 20)

    val1 = random.randint(-15, 15)
    val2 = random.randint(-15, 15)

    constant_K = random.choice([-3, -2, -1, 1, 2, 3])
    constant_K_display = "" if constant_K == 1 else "-" if constant_K == -1 else str(constant_K)

    # Compute answer
    integral_b_c = val2 - val1
    final_answer = constant_K * integral_b_c

    # Question text
    question_text = (
        f"If \\( \\displaystyle \\int_{{{a}}}^{{{b}}} f(x) \\, dx = {val1} \\) and "
        f"\\( \\displaystyle \\int_{{{a}}}^{{{c}}} f(x) \\, dx = {val2} \\) then "
        f"\\( \\displaystyle \\int_{{{b}}}^{{{c}}} {constant_K_display}f(x) \\, dx \\) is equal to:"
    )

    # Format correct answer
    correct_answer_str = f"\\( {final_answer} \\)"

    # Generate distractors
    distractors = set()
    while len(distractors) < 6:
        distractors.update([
            val1 + val2,
            val2 - val1 * constant_K,
            val1 - val2,
            -final_answer,
            final_answer + random.choice([-2, -1, 1, 2]),
            val1 * constant_K,
            val2 * constant_K,
            val1 + val2 * constant_K
        ])
        distractors.discard(final_answer)

    distractor_strings = [f"\\( {int(round(d))} \\)" for d in list(distractors) if isinstance(d, (int, float))]

    # Compose answers list: correct answer first
    answers = [correct_answer_str] + random.sample(distractor_strings, 3)

    return MultipleChoice(question_text, answers, question_type="Definite Integrals")

# 5
def generate_range_composite_question() -> MultipleChoice:
    a = random.choice([i for i in range(-5, 6) if i != 0])
    b = random.choice([i for i in range(-5, 6) if i != 0])
    c = random.choice([i for i in range(-5, 6) if i != 0])

    f = sp.sqrt(a * x + b) + c
    f_latex = sp.latex(f)

    # Domain: ax + b >= 0 => x >= -b/a (a > 0 in this setup)
    # So min value of f(x) is sqrt(0) = 0

    question = f"Find the range of the function \( f(x) = {f_latex} \)"

    correct = f"\( [{c}, \\infty) \)"
    wrong1 = f"\( [{sp.Rational(-b, a)}, \\infty) \)"
    wrong2 = f"\( (0, \\infty) \)"
    wrong3 = f"\( [{sp.latex(b + c)}, \\infty) \)"

    answers = [correct, wrong1, wrong2, wrong3]
    return MultipleChoice(question, answers) 

# 7
def generate_multiple_choice_dice_probability() -> MultipleChoice:
    # Roll two fair dice
    sides1 = random.choice([4, 6, 8, 10, 12, 20])  # First die
    sides2 = random.choice([3, 4])  # Second die

    total_outcomes = sides1 * sides2

    target_sum = random.randint(2, sides1 + sides2)  # Pick a reasonable sum to ask about

    # Count favorable outcomes
    favorable = 0
    for i in range(1, sides1 + 1):
        for j in range(1, sides2 + 1):
            if i + j == target_sum:
                favorable += 1

    correct_prob = sp.Rational(favorable, total_outcomes)

    q = f"A fair die with {sides1} sides and another with {sides2} sides are rolled. What is the probability that the sum of the two dice is {target_sum}?"

    # Generate distractors
    wrong_answers = set()
    while len(wrong_answers) < 3:
        num = random.randint(1, total_outcomes)
        denom = total_outcomes
        wrong = sp.Rational(num, denom)
        if wrong != correct_prob:
            wrong_answers.add(wrong)

    answers = [f"\( {sp.latex(correct_prob)} \)"] + [f"\( {sp.latex(ans)} \)" for ans in wrong_answers]

    return MultipleChoice(q, answers, question_type="Probability")

# 8
def generate_multiple_choice_deck_question() -> MultipleChoice:
    total_cards = 52
    question_type = "probability"

    q_type = random.choice(["no_face_in_two", "given_ace_next_black", "both_red_in_two"])

    if q_type == "no_face_in_two":
        # Q: Probability that neither of two drawn cards is a face card (J/Q/K)?
        face_cards = 12
        non_face = total_cards - face_cards  # 40
        total_ways = comb(total_cards, 2)
        success_ways = comb(non_face, 2)
        prob = sp.Rational(success_ways, total_ways)

        q = "Two cards are drawn at random without replacement. What is the probability that neither is a face card (J, Q, or K)?"
        answers = [
            f"\\( {sp.latex(prob)} \\)",  # correct
            f"\\( {sp.latex(sp.Rational(comb(40,1)*comb(12,1), total_ways))} \\)",
            f"\\( {sp.latex(sp.Rational(comb(12,2), total_ways))} \\)",
            f"\\( {sp.latex(sp.Rational(1,4))} \\)"
        ]

    elif q_type == "given_ace_next_black":
        # Q: If the first card is an ace, what is the probability the next is black?
        black_cards = 26
        q = "A card is drawn and is known to be an ace. What is the probability that the next card drawn is black (without replacement)?"
        # After removing 1 ace, 51 cards remain.
        prob = sp.Rational(26, 51)
        answers = [
            f"\\( {sp.latex(prob)} \\)",
            f"\\( {sp.latex(sp.Rational(25, 51))} \\)",
            f"\\( {sp.latex(sp.Rational(26, 52))} \\)",
            f"\\( {sp.latex(sp.Rational(1,2))} \\)"
        ]

    elif q_type == "both_red_in_two":
        # Q: Probability both cards drawn are red
        red_cards = 26
        total_ways = comb(total_cards, 2)
        red_ways = comb(red_cards, 2)
        prob = sp.Rational(red_ways, total_ways)

        q = "Two cards are drawn randomly without replacement. What is the probability that both are red?"
        answers = [
            f"\\( {sp.latex(prob)} \\)",  # correct
            f"\\( {sp.latex(sp.Rational(26, 52))} \\)",
            f"\\( {sp.latex(sp.Rational(1, 4))} \\)",
            f"\\( {sp.latex(sp.Rational(comb(26,1)*comb(26,1), total_ways))} \\)"
        ]

    return MultipleChoice(q, answers, question_type)

# 10
def generate_multiple_choice_10() -> MultipleChoice:
    # Define the scenario
    total_people = random.randint(40, 100)
    num_A_and_B = random.randint(5, total_people // 4)
    num_B = random.randint(num_A_and_B + 5, total_people - 5)

    # Ensure valid numbers
    while num_B > total_people or num_A_and_B > num_B:
        num_A_and_B = random.randint(5, total_people // 4)
        num_B = random.randint(num_A_and_B + 5, total_people - 5)

    # Compute conditional probability P(A|B)
    prob = sp.Rational(num_A_and_B, num_B)

    q = (
        f"In a group of {total_people} people, {num_B} like event B, "
        f"and {num_A_and_B} like both event A and B. "
        f"What is the probability that a randomly selected person who likes B also likes A?"
    )

    # Generate answer choices
    answers = [
        f"\( {sp.latex(prob)} \)",  # correct answer
        f"\( {sp.latex(sp.Rational(num_A_and_B, total_people))} \)",
        f"\( {sp.latex(sp.Rational(num_B, total_people))} \)",
        f"\( {sp.latex(sp.Rational(total_people, num_B))} \)"
    ]

    return MultipleChoice(q, answers, question_type="Conditional Probability")

def generate_multiple_choice_confidence_interval() -> MultipleChoice:
    # Randomly generate sample mean, sample size, std deviation
    mean = round(random.uniform(10, 100), 2)
    std_dev = round(random.uniform(5, 20), 2)
    n = random.randint(25, 100)

    # z-value for 95% confidence (approximate)
    z = 1.96
    
    # Calculate margin of error
    margin_error = round(z * (std_dev / (n ** 0.5)), 2)
    
    lower_bound = round(mean - margin_error, 2)
    upper_bound = round(mean + margin_error, 2)
    
    question = (f"A sample of size {n} has a sample mean of {mean} "
                f"and a population standard deviation of {std_dev}. "
                f"What is the 95% confidence interval for the population mean?")
    
    # Correct answer: the calculated confidence interval
    correct = f"({lower_bound}, {upper_bound})"
    
    # Generate plausible distractors by varying bounds slightly
    distractor1 = f"({round(lower_bound - 1, 2)}, {upper_bound})"
    distractor2 = f"({lower_bound}, {round(upper_bound + 1, 2)})"
    distractor3 = f"({round(lower_bound + 1, 2)}, {round(upper_bound - 1, 2)})"
    
    answers = [correct, distractor1, distractor2, distractor3]

    return MultipleChoice(question, answers, question_type="95% Confidence Interval")

def generate_multiple_choice() -> MultipleChoice:
    functions = [
        generate_multiple_choice_0, 
        generate_multiple_choice_2, 
        generate_multiple_choice_3, 
        generate_multiple_choice_4, 
        generate_range_composite_question, 
        generate_multiple_choice_dice_probability,
        generate_multiple_choice_deck_question,
        generate_multiple_choice_10,
        generate_multiple_choice_confidence_interval
    ]

    result = random.choice(functions)()
    return result

def questions_html(count: int) -> str:
    result = ""

    for i in range(count):
        mcq = generate_multiple_choice()
        result += f"""
            <div class="question-container">
            <p><b>Question {i + 1}.</b> {mcq.question}</p>
            <label><input type="radio" name="q{i}" value="A"> A. {mcq.a}</label>
            <label><input type="radio" name="q{i}" value="B"> B. {mcq.b}</label>
            <label><input type="radio" name="q{i}" value="C"> C. {mcq.c}</label>
            <label><input type="radio" name="q{i}" value="D"> D. {mcq.d}</label>
            </div>
            """

    return result 