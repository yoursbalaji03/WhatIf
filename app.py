from flask import Flask, render_template, request

from simulation import calculate_scenarios

from database import (
    create_database,
    save_simulation,
    get_simulations
)


app = Flask(__name__)

create_database()


@app.route("/")
def home():

    return render_template(
        "index.html",
        page="home"
    )


@app.route("/simulate", methods=["POST"])
def simulate():

    decision = request.form["decision"]

    savings = float(request.form["savings"])
    income = float(request.form["income"])
    expenses = float(request.form["expenses"])
    cost = float(request.form["cost"])

    months = int(request.form["months"])


    results = calculate_scenarios(
        savings,
        income,
        expenses,
        cost,
        months
    )


    # Save simulation

    save_simulation(
        decision,
        savings,
        income,
        expenses,
        cost,
        months,
        results["recommendation"]
    )


    return render_template(
        "index.html",

        page="result",

        decision=decision,

        months=months,

        results=results
    )


@app.route("/history")
def history():

    simulations = get_simulations()

    return render_template(
        "index.html",

        page="history",

        simulations=simulations
    )


@app.route("/compare", methods=["GET", "POST"])
def compare():

    if request.method == "GET":

        return render_template(
            "index.html",
            page="compare"
        )


    decision1 = request.form["decision1"]
    decision2 = request.form["decision2"]
    decision3 = request.form["decision3"]


    cost1 = float(request.form["cost1"])
    cost2 = float(request.form["cost2"])
    cost3 = float(request.form["cost3"])


    savings = float(request.form["savings"])
    income = float(request.form["income"])
    expenses = float(request.form["expenses"])

    months = int(request.form["months"])


    result1 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost1,
        months
    )

    result2 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost2,
        months
    )

    result3 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost3,
        months
    )


    options = [

        {
            "name": decision1,
            "cost": cost1,
            "value": result1["buy_now"]["normal"],
            "risk": result1["buy_now"]["risk"],
            "risk_score": result1["buy_now"]["risk_score"]
        },

        {
            "name": decision2,
            "cost": cost2,
            "value": result2["buy_now"]["normal"],
            "risk": result2["buy_now"]["risk"],
            "risk_score": result2["buy_now"]["risk_score"]
        },

        {
            "name": decision3,
            "cost": cost3,
            "value": result3["buy_now"]["normal"],
            "risk": result3["buy_now"]["risk"],
            "risk_score": result3["buy_now"]["risk_score"]
        }

    ]


    options.sort(
        key=lambda x: x["value"],
        reverse=True
    )


    best_option = options[0]


    return render_template(
        "index.html",

        page="compare_result",

        options=options,

        best_option=best_option,

        months=months
    )


if __name__ == "__main__":

    app.run(debug=True)