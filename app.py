from flask import Flask, render_template, request, jsonify
from math import exp, factorial

app = Flask(__name__, static_folder='static', template_folder='templates')

def probabilitas_poisson(lam, k):
    return (lam ** k * exp(-lam)) / factorial(k)

def distribusi_poisson(lam, k, jenis_prob):
    langkah = {}
    if jenis_prob == "exact":
        prob = probabilitas_poisson(lam, k)
        langkah["rumus"] = r"\small P(X = x) = \large \frac{e^{-\lambda} \cdot \lambda^x}{x!}"
        langkah["langkah1"] = f"\small P({k}) = \large \\frac{{(2.718)^{{-{int(lam)}}} \\cdot ({int(lam)})^{int(k)}}}{{{int(k)}!}}"
        langkah["langkah2"] = f"\small P({k}) = \large \\frac{{{round(exp(-lam), 3)} \\cdot {int(round(lam ** k)) if lam ** k == int(lam ** k) else round(lam ** k, 3)}}}{{{int(k)}!}} \\Rightarrow \small P({k}) = \large \\frac{{{round(exp(-lam) * (lam ** k), 3)}}}{{{factorial(int(k))}}} \\Rightarrow \small P({k}) = \small {round(prob, 5)}"
    elif jenis_prob == "less_than":
        prob = sum(probabilitas_poisson(lam, i) for i in range(k))
        langkah["rumus"] = r"\small P(X = x) = \large \frac{e^{-\lambda} \cdot \lambda^x}{x!}"
        langkah["steps"] = []
        for i in range(k):
            langkah["steps"].append(f"\small P({i}) = \large \\frac{{(2.718)^{{-{int(lam)}}} \\cdot ({int(lam)})^{int(i)}}}{{{int(i)}!}} \\newline \\Rightarrow \small P({i}) = {round(probabilitas_poisson(lam, i), 5)}")
        langkah["summary"] = f"\small P(x < {int(k)}) = " + " + ".join([f"P({i})" for i in range(k)]) + f" = \\small {round(prob, 5)}"
    elif jenis_prob == "at_most":
        prob = sum(probabilitas_poisson(lam, i) for i in range(k + 1))
        langkah["rumus"] = r"\small P(X = x) = \large \frac{e^{-\lambda} \cdot \lambda^x}{x!}"
        langkah["langkah1"] = f"\small P({k}) = \large \\frac{{(2.718)^{{-{int(lam)}}} \\cdot ({int(lam)})^{int(k)}}}{{{int(k)}!}}"
        langkah["steps"] = []
        for i in range(k + 1):
            langkah["steps"].append(f"\small P({i}) = \large \\frac{{(2.718)^{{-{int(lam)}}} \\cdot ({int(lam)})^{int(i)}}}{{{int(i)}!}} \\newline \\Rightarrow \small P({i}) = {round(probabilitas_poisson(lam, i), 5)}")
        langkah["summary"] = f"\small P(x \leq {int(k)}) = " + " + ".join([f"P({i})" for i in range(k + 1)]) + f" = \\small {round(prob, 5)}"
    elif jenis_prob == "greater_than":
        prob = 1 - sum(probabilitas_poisson(lam, i) for i in range(k + 1))
        langkah["rumus"] = r"\small P(X = x) = \large \frac{e^{-\lambda} \cdot \lambda^k}{x!}"
        langkah["summary"] = f"P(X > {int(k)}) = 1 - P(X \\leq {int(k)}) = {round(prob, 5)}"
        langkah["hasil"] = f"\\small P(x > {int(k)}) = {round(prob, 5)}"
    elif jenis_prob == "at_least":
        prob = 1 - sum(probabilitas_poisson(lam, i) for i in range(k))
        langkah["rumus"] = r"\small P(X = x) = \large \frac{e^{-\lambda} \cdot \lambda^x}{x!}"
        langkah["summary"] = f"P(X \\geq {int(k)}) = 1 - P(X < {int(k)}) = {round(prob, 5)}"
        langkah["hasil"] = f"P(X \\geq {int(k)}) = {round(prob, 5)}"
    else:
        prob = 0
    langkah["hasil"] = f"\\small P(x = {int(k)}) = {round(prob, 5)}"
    return prob, langkah

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        try:
            jenis_probabilitas = data.get('probability_type')
            lam = float(data.get('lam'))
            x = int(data.get('x'))

            if lam < 0 or x < 0:
                return jsonify({"error": "λ dan x harus bernilai positif."}), 400

            prob, langkah = distribusi_poisson(lam, x, jenis_probabilitas)
            return jsonify({"hasil": langkah["hasil"], "langkah": langkah})
        except (ValueError, TypeError):
            return jsonify({"error": "Input tidak valid."}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
