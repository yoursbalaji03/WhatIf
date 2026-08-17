from flask import Flask, render_template, request

from simulation import (
    calculate_scenarios,
    calculate_investment_plans
)

from database import (
    create_database,
    save_simulation,
    get_simulations
)


app = Flask(__name__)

create_database()


# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        page="home"
    )


# =========================================
# SIMULATE
# =========================================

@app.route("/simulate", methods=["POST"])
def simulate():

    decision = request.form["decision"]

    salary = float(
        request.form["salary"]
    )

    earning_months = int(
        request.form["earning_months"]
    )

    cost = float(
        request.form["cost"]
    )

    simulation_months = int(
        request.form["months"]
    )

    investment_goal = request.form.get(
        "investment_goal",
        "long"
    )

    investment_risk = request.form.get(
        "investment_risk",
        "medium"
    )


    # =====================================
    # CALCULATE EVERYTHING
    # =====================================

    results = calculate_scenarios(

        salary,

        earning_months,

        cost,

        simulation_months,

        investment_goal,

        investment_risk

    )


    # =====================================
    # SAVE HISTORY
    # =====================================

    try:

        save_simulation(

            decision,

            results["past_savings"],

            salary,

            results["expenses"],

            cost,

            simulation_months,

            results["recommendation"]

        )

    except Exception as e:

        print(
            "History save skipped:",
            e
        )


    # =====================================
    # SHOW RESULT
    # =====================================

    return render_template(

        "index.html",

        page="result",

        decision=decision,

        months=simulation_months,

        results=results

    )


# =========================================
# HISTORY
# =========================================

@app.route("/history")
def history():

    try:

        simulations = get_simulations()

    except Exception as e:

        print(
            "History error:",
            e
        )

        simulations = []


    return render_template(

        "index.html",

        page="history",

        simulations=simulations

    )


# =========================================
# INVESTMENTS
# =========================================

@app.route("/investments", methods=["GET", "POST"])
def investments():

    if request.method == "GET":

        return render_template(

            "index.html",

            page="investments"

        )


    salary = float(
        request.form["salary"]
    )

    months = int(
        request.form["months"]
    )

    custom_return = request.form.get(
        "custom_return"
    )

    if custom_return:

        custom_return = float(
            custom_return
        )

    else:

        custom_return = None


    result = (
        calculate_investment_plans(
            salary,
            months,
            custom_return
        )
    )


    return render_template(

        "index.html",

        page="investment_result",

        salary=salary,

        months=months,

        result=result

    )


# =========================================
# COMPARE PAGE
# =========================================

@app.route("/compare", methods=["GET", "POST"])
def compare():

    if request.method == "GET":

        return render_template(

            "index.html",

            page="compare"

        )


    # =====================================
    # OPTIONS
    # =====================================

    decision1 = request.form["decision1"]

    decision2 = request.form["decision2"]

    decision3 = request.form["decision3"]


    cost1 = float(
        request.form["cost1"]
    )

    cost2 = float(
        request.form["cost2"]
    )

    cost3 = float(
        request.form["cost3"]
    )


    # =====================================
    # FINANCIAL DETAILS
    # =====================================

    salary = float(
        request.form["salary"]
    )

    earning_months = int(
        request.form["earning_months"]
    )

    simulation_months = int(
        request.form["months"]
    )


    investment_goal = request.form.get(
        "investment_goal",
        "long"
    )

    investment_risk = request.form.get(
        "investment_risk",
        "medium"
    )


    # =====================================
    # CALCULATE OPTION 1
    # =====================================

    result1 = calculate_scenarios(

        salary,

        earning_months,

        cost1,

        simulation_months,

        investment_goal,

        investment_risk

    )


    # =====================================
    # CALCULATE OPTION 2
    # =====================================

    result2 = calculate_scenarios(

        salary,

        earning_months,

        cost2,

        simulation_months,

        investment_goal,

        investment_risk

    )


    # =====================================
    # CALCULATE OPTION 3
    # =====================================

    result3 = calculate_scenarios(

        salary,

        earning_months,

        cost3,

        simulation_months,

        investment_goal,

        investment_risk

    )


    # =====================================
    # CREATE COMPARISON
    # =====================================

    options = [

        {

            "name":
                decision1,

            "cost":
                cost1,

            "value":
                result1["buy_now"]["normal"],

            "risk":
                result1["buy_now"]["risk"],

            "risk_score":
                result1["buy_now"]["risk_score"]

        },

        {

            "name":
                decision2,

            "cost":
                cost2,

            "value":
                result2["buy_now"]["normal"],

            "risk":
                result2["buy_now"]["risk"],

            "risk_score":
                result2["buy_now"]["risk_score"]

        },

        {

            "name":
                decision3,

            "cost":
                cost3,

            "value":
                result3["buy_now"]["normal"],

            "risk":
                result3["buy_now"]["risk"],

            "risk_score":
                result3["buy_now"]["risk_score"]

        }

    ]


    # =====================================
    # SORT BEST OPTION
    # =====================================

    options.sort(

        key=lambda x:
            x["value"],

        reverse=True

    )


    best_option = options[0]


    # =====================================
    # SHOW COMPARISON
    # =====================================

    return render_template(

        "index.html",

        page="compare_result",

        options=options,

        best_option=best_option,

        months=simulation_months

    )


# =========================================
# START SERVER
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )