import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=100):
    """
    Generates a synthetic transaction dataset for a credit card user.
    Columns: date, amount, category, payment_type, paid_on_time
    """
    np.random.seed(42)
    categories = ['Essential', 'Luxury', 'Bills', 'Entertainment', 'Dining']
    payment_types = ['Full Payment', 'Minimum Due', 'Partial Payment']
    
    start_date = datetime.now() - timedelta(days=180)
    data = []
    
    for i in range(num_records):
        date = start_date + timedelta(days=i * (180/num_records))
        category = np.random.choice(categories, p=[0.4, 0.1, 0.2, 0.15, 0.15])
        
        # Spending logic: Luxury is more expensive
        if category == 'Luxury':
            amount = np.random.uniform(500, 2000)
        elif category == 'Essential':
            amount = np.random.uniform(20, 200)
        else:
            amount = np.random.uniform(10, 500)
            
        payment_type = np.random.choice(payment_types, p=[0.7, 0.2, 0.1])
        # Higher probability of on-time payment if it's 'Full Payment'
        if payment_type == 'Full Payment':
            paid_on_time = np.random.choice([True, False], p=[0.95, 0.05])
        else:
            paid_on_time = np.random.choice([True, False], p=[0.6, 0.4])
            
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'amount': round(amount, 2),
            'category': category,
            'payment_type': payment_type,
            'paid_on_time': paid_on_time
        })
        
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df
