import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_repayment_score(df):
    """
    Calculates Repayment Score (0-100)
    - % on-time payments
    - payment type weight (Full Payment > Minimum > Partial)
    """
    on_time_ratio = df['paid_on_time'].mean() * 100
    
    type_weights = {
        'Full Payment': 1.0,
        'Minimum Due': 0.5,
        'Partial Payment': 0.2
    }
    avg_payment_weight = df['payment_type'].map(type_weights).mean() * 100
    
    # Combined Repayment Score (60% on-time, 40% payment type quality)
    score = (on_time_ratio * 0.6) + (avg_payment_weight * 0.4)
    return min(100, max(0, score))

def calculate_utilization_ratio(df, current_limit):
    """
    Calculates Credit Utilization Ratio.
    Lower is better for credit score (Ideal < 30%).
    """
    # Sum of last 30 days spending
    recent_spending = df[df['date'] > (df['date'].max() - pd.Timedelta(days=30))]['amount'].sum()
    
    ratio = (recent_spending / current_limit) * 100
    return ratio

def calculate_stability_score(df):
    """
    Calculates Spending Stability Score based on monthly variance.
    High variance = Lower stability.
    """
    df['month'] = df['date'].dt.to_period('M')
    monthly_spending = df.groupby('month')['amount'].sum()
    
    if len(monthly_spending) < 2:
        return 100.0 # Not enough data, assume stable
        
    variance = monthly_spending.std() / monthly_spending.mean() # Coefficient of variation
    # Score: 100 - (CV * 100), capped at 0-100
    score = 100 - (variance * 100)
    return min(100, max(0, score))

def calculate_growth_trend(df):
    """
    Calculates Spending Growth Trend using Linear Regression slope.
    """
    df['month_num'] = (df['date'].dt.year - df['date'].dt.year.min()) * 12 + df['date'].dt.month
    monthly_spending = df.groupby('month_num')['amount'].sum().reset_index()
    
    if len(monthly_spending) < 2:
        return 0.0
        
    X = monthly_spending[['month_num']].values
    y = monthly_spending['amount'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    return float(model.coef_[0])

def calculate_category_weight_score(df):
    """
    Calculates Lifestyle Category Weight.
    Essential vs Luxury ratio.
    """
    category_totals = df.groupby('category')['amount'].sum()
    essential = category_totals.get('Essential', 0) + category_totals.get('Bills', 0)
    luxury = category_totals.get('Luxury', 0)
    
    total = df['amount'].sum()
    if total == 0: return 100
    
    # More essential spending relative to luxury is better for stability
    essential_ratio = essential / total
    luxury_ratio = luxury / total
    
    # Score favors high essential and low luxury
    score = (essential_ratio * 100) + ((1 - luxury_ratio) * 100)
    return min(100, max(0, score / 2))

def get_comprehensive_score(df, current_limit):
    """
    Combines all scores into a final Credit Score (0-100).
    """
    repayment = calculate_repayment_score(df)
    utilization = calculate_utilization_ratio(df, current_limit)
    stability = calculate_stability_score(df)
    growth = calculate_growth_trend(df)
    lifestyle = calculate_category_weight_score(df)
    
    # Utilization score (Inverse: 100 is best, which means < 30% usage)
    if utilization <= 30:
        util_score = 100
    elif utilization <= 70:
        util_score = 70 - (utilization - 30)
    else:
        util_score = 30 - (utilization - 70)
    util_score = min(100, max(0, util_score))
    
    # Weights
    # 40% Repayment, 30% Utilization, 15% Stability, 10% Lifestyle, 5% Growth (stability of growth)
    final_score = (repayment * 0.40) + \
                  (util_score * 0.30) + \
                  (stability * 0.15) + \
                  (lifestyle * 0.10) + \
                  (50 if growth < 100 else 0) # Simple growth penalty if too aggressive
                  
    return {
        'final_score': round(final_score, 2),
        'repayment_score': round(repayment, 2),
        'utilization_ratio': round(utilization, 2),
        'stability_score': round(stability, 2),
        'growth_trend': round(growth, 2),
        'lifestyle_score': round(lifestyle, 2)
    }
