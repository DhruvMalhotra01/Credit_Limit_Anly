def generate_credit_decision(score, current_limit):
    """
    Generates a credit decision based on the final credit score and current limit.
    Returns: (score, recommended_limit, explanation_text)
    """
    if score < 40:
        recommended_limit = current_limit * 0.8 # 20% decrease
        explanation_text = "Due to a high risk score and inconsistent repayment behavior, we recommend reducing the credit limit to mitigate exposure."
    elif 40 <= score < 65:
        recommended_limit = current_limit
        explanation_text = "The credit profile is stable but does not yet qualify for an increase. We recommend maintaining the current limit while monitoring performance."
    elif 65 <= score < 80:
        recommended_limit = current_limit * 1.25 # 25% increase
        explanation_text = "Strong repayment history and low utilization justify a moderate increase in the credit limit."
    elif 80 <= score < 90:
        recommended_limit = current_limit * 1.50 # 50% increase
        explanation_text = "Excellent financial behavior and high stability scores qualify for a significant limit expansion."
    else: # 90+
        recommended_limit = current_limit * 2.0 # 100% increase / Premium
        explanation_text = "Exceptional creditworthiness detected. The user is eligible for a premium tier upgrade with a doubled credit limit."
        
    return score, round(recommended_limit, 2), explanation_text
