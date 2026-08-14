def calculate_risk_score(
    savings,
    income,
    expenses,
    cost,
    worst_case
):
    """
    Calculate a risk score from 0 to 100.
    Higher score = higher financial risk.
    """

    score = 0

    monthly_surplus = income - expenses

    # --------------------------------
    # 1. COST VS SAVINGS
    # --------------------------------

    if savings > 0:
        cost_ratio = cost / savings

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

    else:
        score += 35


    # --------------------------------
    # 2. MONTHLY SURPLUS
    # --------------------------------

    if monthly_surplus <= 0:
        score += 30

    elif monthly_surplus < income * 0.10:
        score += 25

    elif monthly_surplus < income * 0.20:
        score += 18

    elif monthly_surplus < income * 0.30:
        score += 10

    else:
        score += 5


    # --------------------------------
    # 3. WORST CASE
    # --------------------------------

    if worst_case < 0:
        score += 25

    elif savings > 0 and worst_case < savings * 0.25:
        score += 20

    elif savings > 0 and worst_case < savings * 0.50:
        score += 12

    else:
        score += 5


    # --------------------------------
    # LIMIT SCORE
    # --------------------------------

    score = min(score, 100)


    # --------------------------------
    # RISK LEVEL
    # --------------------------------

    if score >= 70:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    else:
        level = "LOW"


    return score, level


def calculate_scenarios(
    savings,
    income,
    expenses,
    cost,
    months
):

    monthly_saving = income - expenses


    # =================================
    # NORMAL CASE
    # =================================

    buy_now_normal = savings - cost

    wait_normal = savings

    normal_buy_months = []
    normal_wait_months = []


    for month in range(1, months + 1):

        buy_now_normal += monthly_saving

        wait_normal += monthly_saving

        normal_buy_months.append(
            round(buy_now_normal, 2)
        )

        normal_wait_months.append(
            round(wait_normal, 2)
        )


    # =================================
    # BEST CASE
    # =================================

    best_income = income * 1.20

    best_expenses = expenses * 0.90

    best_monthly_saving = (
        best_income - best_expenses
    )

    buy_now_best = savings - cost

    wait_best = savings


    for month in range(months):

        buy_now_best += best_monthly_saving

        wait_best += best_monthly_saving


    # =================================
    # WORST CASE
    # =================================

    worst_income = income * 0.80

    worst_expenses = expenses * 1.20

    worst_monthly_saving = (
        worst_income - worst_expenses
    )

    buy_now_worst = savings - cost

    wait_worst = savings


    for month in range(months):

        buy_now_worst += worst_monthly_saving

        wait_worst += worst_monthly_saving


    # =================================
    # SMART RISK SCORE
    # =================================

    buy_risk_score, buy_risk = calculate_risk_score(
        savings,
        income,
        expenses,
        cost,
        buy_now_worst
    )


    wait_risk_score, wait_risk = calculate_risk_score(
        savings,
        income,
        expenses,
        0,
        wait_worst
    )


    # =================================
    # RECOMMENDATION
    # =================================

    if (
        buy_risk_score < wait_risk_score
        and buy_now_normal >= wait_normal * 0.8
    ):

        recommendation = "BUY NOW"

    else:

        recommendation = "WAIT"
    # =================================
    # DECISION EXPLANATIONS
    # =================================

    reasons = []

    monthly_surplus = income - expenses

    # Reason 1: Cost vs savings
    if cost > savings:
        reasons.append(
            "The purchase cost is higher than your current savings."
        )
    elif cost > savings * 0.50:
        reasons.append(
            "The purchase uses a large portion of your current savings."
        )
    else:
        reasons.append(
            "The purchase does not consume most of your current savings."
        )


    # Reason 2: Monthly surplus
    if monthly_surplus <= 0:
        reasons.append(
            "Your monthly expenses are equal to or higher than your income."
        )
    elif monthly_surplus < income * 0.20:
        reasons.append(
            f"Your monthly surplus is only ₹{monthly_surplus:,.0f}."
        )
    else:
        reasons.append(
            f"Your monthly surplus is ₹{monthly_surplus:,.0f}, giving you some financial flexibility."
        )


    # Reason 3: Compare outcomes
    difference = wait_normal - buy_now_normal

    if difference > 0:
        reasons.append(
            f"Waiting leaves you approximately ₹{difference:,.0f} more after {months} months."
        )
    else:
        reasons.append(
            f"Buying now leaves you approximately ₹{abs(difference):,.0f} more after {months} months."
        )


    # Reason 4: Risk
    if buy_risk_score >= 70:
        reasons.append(
            f"Buying now has a HIGH risk score of {buy_risk_score}/100."
        )

    elif buy_risk_score >= 40:
        reasons.append(
            f"Buying now has a MEDIUM risk score of {buy_risk_score}/100."
        )

    else:
        reasons.append(
            f"Buying now has a LOW risk score of {buy_risk_score}/100."
        )


    # Final explanation
    if recommendation == "BUY NOW":

        explanation = (
            "The system recommends BUY NOW because the purchase "
            "has an acceptable risk level and the projected outcome "
            "is financially reasonable."
        )

    else:

        explanation = (
            "The system recommends WAIT because waiting provides "
            "a safer financial position based on the simulated outcomes."
        )


    # =================================
    # RETURN RESULTS
    # =================================

    return {

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

            "risk": buy_risk,

            "risk_score": buy_risk_score
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

            "risk": wait_risk,

            "risk_score": wait_risk_score
        },


        "monthly": {

            "buy_now":
                normal_buy_months,

            "wait":
                normal_wait_months
        },


               "recommendation":
            recommendation,

        "reasons":
            reasons,

        "explanation":
            explanation

    }