def calculate_risk_score(
    current_savings,
    monthly_savings,
    cost,
    worst_case
):
    """
    Risk score:
    0-39   = LOW
    40-69  = MEDIUM
    70-100 = HIGH
    """

    score = 0

    # =================================
    # COST VS CURRENT SAVINGS
    # =================================

    if current_savings <= 0:

        score += 35

    else:

        cost_ratio = cost / current_savings

        if cost_ratio >= 1:
            score += 35

        elif cost_ratio >= 0.75:
            score += 28

        elif cost_ratio >= 0.50:
            score += 20

        elif cost_ratio >= 0.25:
            score += 10

        else:
            score += 5


    # =================================
    # MONTHLY SAVING CAPACITY
    # =================================

    if monthly_savings <= 0:

        score += 30

    elif monthly_savings < 5000:

        score += 25

    elif monthly_savings < 10000:

        score += 18

    elif monthly_savings < 15000:

        score += 10

    else:

        score += 5


    # =================================
    # WORST CASE
    # =================================

    if worst_case < 0:

        score += 35

    elif (
        current_savings > 0
        and worst_case < current_savings * 0.25
    ):

        score += 25

    elif (
        current_savings > 0
        and worst_case < current_savings * 0.50
    ):

        score += 15

    else:

        score += 5


    score = min(score, 100)


    if score >= 70:

        level = "HIGH"

    elif score >= 40:

        level = "MEDIUM"

    else:

        level = "LOW"


    return score, level


# =================================
# INVESTMENT RECOMMENDATION
# =================================

def investment_recommendation(
    salary,
    goal="long",
    risk="medium"
):

    investment_amount = salary * 0.10

    goal = str(goal).lower()

    risk = str(risk).lower()


    # =================================
    # SHORT TERM
    # =================================

    if goal == "short":

        if risk == "low":

            category = (
                "Safer / liquid investment options"
            )

            reason = (
                "Your goal is short term and your "
                "risk preference is low, so capital "
                "preservation and easy access are prioritized."
            )

        elif risk == "medium":

            category = (
                "Conservative diversified options"
            )

            reason = (
                "Your short-term goal requires relatively "
                "controlled risk while allowing some growth."
            )

        else:

            category = (
                "Higher-risk exposure is generally "
                "unsuitable for a short-term goal"
            )

            reason = (
                "Short investment periods provide less "
                "time to recover from market declines."
            )


    # =================================
    # MEDIUM TERM
    # =================================

    elif goal == "medium":

        if risk == "low":

            category = (
                "Debt-oriented investment options"
            )

            reason = (
                "Your medium-term goal and low risk "
                "preference favor relatively stable investments."
            )

        elif risk == "medium":

            category = (
                "Hybrid / diversified investment options"
            )

            reason = (
                "A medium-term goal with moderate risk "
                "can consider a diversified mix of asset classes."
            )

        else:

            category = (
                "Diversified equity-oriented options"
            )

            reason = (
                "Your higher risk tolerance allows greater "
                "exposure to growth-oriented investments."
            )


    # =================================
    # LONG TERM
    # =================================

    else:

        if risk == "low":

            category = (
                "Diversified conservative options"
            )

            reason = (
                "Your long-term horizon provides time for growth, "
                "while your low risk preference calls for caution."
            )

        elif risk == "medium":

            category = (
                "Diversified / index-oriented options"
            )

            reason = (
                "A long-term horizon and moderate risk preference "
                "can support diversified growth-oriented investing."
            )

        else:

            category = (
                "Diversified equity-oriented options"
            )

            reason = (
                "A long-term horizon gives more time to potentially "
                "absorb market volatility, consistent with your "
                "higher risk preference."
            )


    return {

        "monthly_amount": round(
            investment_amount,
            2
        ),

        "category": category,

        "reason": reason,

        "goal": goal,

        "risk": risk

    }


# =================================
# INVESTMENT PLANS
# =================================

INVESTMENT_PLANS = [
    {
        "name": "PPF",
        "full_name": "Public Provident Fund",
        "annual_return": 7.1,
        "risk_level": "Low",
        "risk_score": 15,
        "min_amount": 500,
        "lock_in": "15 years",
        "description": "Government-backed, tax-free savings scheme with guaranteed returns."
    },
    {
        "name": "FD",
        "full_name": "Fixed Deposit",
        "annual_return": 7.0,
        "risk_level": "Low",
        "risk_score": 10,
        "min_amount": 1000,
        "lock_in": "Varies (7 days - 10 years)",
        "description": "Bank deposit with fixed interest rate and guaranteed returns."
    },
    {
        "name": "Gold",
        "full_name": "Gold (SGB / ETF)",
        "annual_return": 10.0,
        "risk_level": "Medium",
        "risk_score": 40,
        "min_amount": 100,
        "lock_in": "No lock-in (SGB: 8 years)",
        "description": "Hedge against inflation, performs well during economic uncertainty."
    },
    {
        "name": "SIP",
        "full_name": "Mutual Fund SIP",
        "annual_return": 12.0,
        "risk_level": "Medium",
        "risk_score": 50,
        "min_amount": 500,
        "lock_in": "No lock-in (ELSS: 3 years)",
        "description": "Systematic investment in diversified mutual fund schemes."
    },
    {
        "name": "Stocks",
        "full_name": "Direct Equity",
        "annual_return": 15.0,
        "risk_level": "High",
        "risk_score": 75,
        "min_amount": 100,
        "lock_in": "No lock-in",
        "description": "Direct stock market investment with highest potential returns and risk."
    },
    {
        "name": "NPS",
        "full_name": "National Pension System",
        "annual_return": 9.0,
        "risk_level": "Medium",
        "risk_score": 45,
        "min_amount": 1000,
        "lock_in": "Until age 60",
        "description": "Government pension scheme with tax benefits and market-linked returns."
    }
]


def calculate_investment_plans(
    salary,
    months,
    custom_return=None
):
    """
    Calculate projected returns for all investment plans
    based on 10% of salary.
    """

    monthly_investment = salary * 0.10

    plans = []


    for plan in INVESTMENT_PLANS:

        monthly_rate = (
            plan["annual_return"]
            / 100
            / 12
        )


        balance = 0

        monthly_values = []

        total_invested = 0


        for month in range(1, months + 1):

            balance = (
                balance
                * (1 + monthly_rate)
                + monthly_investment
            )

            total_invested += (
                monthly_investment
            )

            monthly_values.append(
                round(balance, 2)
            )


        total_returns = (
            round(
                balance - total_invested,
                2
            )
        )

        plans.append({

            "name": plan["name"],

            "full_name": plan["full_name"],

            "annual_return": plan["annual_return"],

            "risk_level": plan["risk_level"],

            "risk_score": plan["risk_score"],

            "min_amount": plan["min_amount"],

            "lock_in": plan["lock_in"],

            "description": plan["description"],

            "monthly_investment": round(
                monthly_investment,
                2
            ),

            "total_invested": round(
                total_invested,
                2
            ),

            "projected_value": round(
                balance,
                2
            ),

            "total_returns": total_returns,

            "monthly_values": monthly_values

        })


    # =================================
    # CUSTOM PLAN
    # =================================

    if custom_return is not None:

        custom_rate = (
            float(custom_return) / 100 / 12
        )

        balance = 0

        monthly_values = []

        total_invested = 0


        for month in range(1, months + 1):

            balance = (
                balance
                * (1 + custom_rate)
                + monthly_investment
            )

            total_invested += (
                monthly_investment
            )

            monthly_values.append(
                round(balance, 2)
            )


        total_returns = (
            round(
                balance - total_invested,
                2
            )
        )

        plans.append({

            "name": "Custom",

            "full_name": "Custom Investment",

            "annual_return": float(
                custom_return
            ),

            "risk_level": "User Defined",

            "risk_score": 50,

            "min_amount": 0,

            "lock_in": "Flexible",

            "description": (
                "Your custom investment with "
                f"{custom_return}% expected "
                "annual returns."
            ),

            "monthly_investment": round(
                monthly_investment,
                2
            ),

            "total_invested": round(
                total_invested,
                2
            ),

            "projected_value": round(
                balance,
                2
            ),

            "total_returns": total_returns,

            "monthly_values": monthly_values

        })


    # =================================
    # SORT BY PROJECTED VALUE
    # =================================

    plans.sort(
        key=lambda x: x["projected_value"],
        reverse=True
    )


    return {

        "monthly_investment": round(
            monthly_investment,
            2
        ),

        "plans": plans

    }


# =================================
# MAIN SIMULATION
# =================================

def calculate_scenarios(
    salary,
    earning_months,
    cost,
    simulation_months,
    investment_goal="long",
    investment_risk="medium"
):

    salary = float(salary)

    earning_months = int(
        earning_months
    )

    cost = float(cost)

    simulation_months = int(
        simulation_months
    )


    # =================================
    # 60 - 30 - 10 RULE
    # =================================

    expenses = salary * 0.60

    monthly_savings = salary * 0.30

    investment = salary * 0.10


    # =================================
    # PAST SAVINGS
    # =================================

    past_savings = (
        monthly_savings
        * earning_months
    )


    # =================================
    # NORMAL CASE
    # =================================

    buy_now_normal = (
        past_savings
        - cost
    )

    wait_normal = past_savings


    buy_now_months = []

    wait_months = []


    for month in range(
        1,
        simulation_months + 1
    ):

        buy_now_normal += monthly_savings

        wait_normal += monthly_savings


        buy_now_months.append(
            round(
                buy_now_normal,
                2
            )
        )

        wait_months.append(
            round(
                wait_normal,
                2
            )
        )


    # =================================
    # BEST CASE
    # =================================

    best_salary = salary * 1.20

    best_expenses = expenses * 0.90

    best_investment = (
        best_salary * 0.10
    )

    best_monthly_savings = (
        best_salary
        - best_expenses
        - best_investment
    )


    buy_now_best = (
        past_savings
        - cost
    )

    wait_best = past_savings


    for _ in range(
        simulation_months
    ):

        buy_now_best += (
            best_monthly_savings
        )

        wait_best += (
            best_monthly_savings
        )


    # =================================
    # WORST CASE
    # =================================

    worst_salary = salary * 0.80

    worst_expenses = expenses * 1.20

    worst_investment = (
        worst_salary * 0.10
    )

    worst_monthly_savings = (
        worst_salary
        - worst_expenses
        - worst_investment
    )


    buy_now_worst = (
        past_savings
        - cost
    )

    wait_worst = past_savings


    for _ in range(
        simulation_months
    ):

        buy_now_worst += (
            worst_monthly_savings
        )

        wait_worst += (
            worst_monthly_savings
        )


    # =================================
    # RISK
    # =================================

    buy_risk_score, buy_risk = (
        calculate_risk_score(
            past_savings,
            monthly_savings,
            cost,
            buy_now_worst
        )
    )


    wait_risk_score, wait_risk = (
        calculate_risk_score(
            past_savings,
            monthly_savings,
            0,
            wait_worst
        )
    )


    # =================================
    # RECOMMENDATION
    # =================================

    difference = (
        wait_normal
        - buy_now_normal
    )


    if (
        buy_risk_score < 40
        and buy_now_normal >= 0
    ):

        recommendation = "BUY NOW"

    else:

        recommendation = "WAIT"


    # =================================
    # WHY
    # =================================

    reasons = []


    reasons.append(
        f"Your estimated monthly expenses are "
        f"₹{expenses:,.0f} (60% of your salary)."
    )


    reasons.append(
        f"Your estimated monthly savings are "
        f"₹{monthly_savings:,.0f} (30% of your salary)."
    )


    reasons.append(
        f"Your estimated monthly investment allocation "
        f"is ₹{investment:,.0f} (10% of your salary)."
    )


    reasons.append(
        f"Based on {earning_months} months of saving, "
        f"your estimated past savings are "
        f"₹{past_savings:,.0f}."
    )


    if difference > 0:

        reasons.append(
            f"Waiting leaves approximately "
            f"₹{difference:,.0f} more after "
            f"{simulation_months} months."
        )

    else:

        reasons.append(
            f"Buying now produces approximately "
            f"₹{abs(difference):,.0f} more after "
            f"{simulation_months} months."
        )


    reasons.append(
        f"BUY NOW risk score is "
        f"{buy_risk_score}/100 ({buy_risk})."
    )


    reasons.append(
        f"WAIT risk score is "
        f"{wait_risk_score}/100 ({wait_risk})."
    )


    if recommendation == "BUY NOW":

        explanation = (
            "The system recommends BUY NOW because "
            "the purchase remains financially manageable "
            "under the current assumptions."
        )

    else:

        explanation = (
            "The system recommends WAIT because waiting "
            "provides a stronger financial position and/or "
            "lower financial risk."
        )


    # =================================
    # INVESTMENT PLAN
    # =================================

    investment_plan = (
        investment_recommendation(
            salary,
            goal=investment_goal,
            risk=investment_risk
        )
    )


    # =================================
    # INVESTMENT PLANS
    # =================================

    investment_plans = (
        calculate_investment_plans(
            salary,
            simulation_months
        )
    )


    # =================================
    # RETURN RESULTS
    # =================================

    return {

        "salary": round(
            salary,
            2
        ),

        "expenses": round(
            expenses,
            2
        ),

        "monthly_savings": round(
            monthly_savings,
            2
        ),

        "investment": round(
            investment,
            2
        ),

        "earning_months":
            earning_months,

        "past_savings": round(
            past_savings,
            2
        ),


        "buy_now": {

            "best": round(
                buy_now_best,
                2
            ),

            "normal": round(
                buy_now_normal,
                2
            ),

            "worst": round(
                buy_now_worst,
                2
            ),

            "risk":
                buy_risk,

            "risk_score":
                buy_risk_score
        },


        "wait": {

            "best": round(
                wait_best,
                2
            ),

            "normal": round(
                wait_normal,
                2
            ),

            "worst": round(
                wait_worst,
                2
            ),

            "risk":
                wait_risk,

            "risk_score":
                wait_risk_score
        },


        "monthly": {

            "buy_now":
                buy_now_months,

            "wait":
                wait_months
        },


        "recommendation":
            recommendation,

        "reasons":
            reasons,

        "explanation":
            explanation,

        "investment_plan":
            investment_plan,

        "investment_plans":
            investment_plans

    }