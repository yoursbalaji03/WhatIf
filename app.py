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
    return render_template("index.html")


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
        "result.html",
        decision=decision,
        months=months,
        results=results
    )


@app.route("/history")
def history():

    simulations = get_simulations()

    return render_template(
        "history.html",
        simulations=simulations
    )


# -----------------------------------------
# COMPARE DECISIONS
# -----------------------------------------

@app.route("/compare", methods=["GET", "POST"])
def compare():

    if request.method == "GET":

        return render_template("compare.html")


    # Option names
    decision1 = request.form["decision1"]
    decision2 = request.form["decision2"]
    decision3 = request.form["decision3"]

    # Option costs
    cost1 = float(request.form["cost1"])
    cost2 = float(request.form["cost2"])
    cost3 = float(request.form["cost3"])

    # Common financial details
    savings = float(request.form["savings"])
    income = float(request.form["income"])
    expenses = float(request.form["expenses"])
    months = int(request.form["months"])


    # Calculate Option 1

    result1 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost1,
        months
    )


    # Calculate Option 2

    result2 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost2,
        months
    )


    # Calculate Option 3

    result3 = calculate_scenarios(
        savings,
        income,
        expenses,
        cost3,
        months
    )


    # Get normal-case BUY NOW result

    option1_value = result1["buy_now"]["normal"]
    option2_value = result2["buy_now"]["normal"]
    option3_value = result3["buy_now"]["normal"]


    options = [
        {
            "name": decision1,
            "cost": cost1,
            "value": option1_value,
            "risk": result1["buy_now"]["risk"]
        },

        {
            "name": decision2,
            "cost": cost2,
            "value": option2_value,
            "risk": result2["buy_now"]["risk"]
        },

        {
            "name": decision3,
            "cost": cost3,
            "value": option3_value,
            "risk": result3["buy_now"]["risk"]
        }
    ]


    # Sort from highest final savings to lowest

    options.sort(
        key=lambda option: option["value"],
        reverse=True
    )


    best_option = options[0]


    return render_template(
        "compare_result.html",
        options=options,
        best_option=best_option,
        months=months
    )


if __name__ == "__main__":
    app.run(debug=True)