import pandas as pd
import random
import string
from datetime import datetime, timedelta


def generate_client_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def generate_balance():
    return round(random.uniform(1000, 10000), 2)

def generate_date():
    start_date = datetime.now() - timedelta(days=365)
    random_date = start_date + timedelta(days=random.randint(0, 365))
    return random_date.strftime('%Y-%m-%d')

def generate_credits():
    return random.randint(0, 10)

def generate_monthly_income():
    return random.randint(0, 1000000)

def generate_monthly_expenses():
    return random.randint(0, 1000000)

def generate_monthly_loan_rate():
    return random.randint(0, 10000)


data = {
    'client_number': [generate_client_number() for _ in range(1000)],
    'balance': [generate_balance() for _ in range(1000)],
    'last_activity': [generate_date() for _ in range(1000)],
    'Monthly_income': [generate_monthly_income() for _ in range(1000)],
    'Monthly_expenses': [generate_monthly_expenses() for _ in range(1000)],
    'Monthly_loan_rate': [generate_monthly_loan_rate() for _ in range(1000)]
}

df = pd.DataFrame(data)

df['last_activity'] = pd.to_datetime(df['last_activity'], format='%Y-%m-%d')
current_date = datetime.now()
df['days_since_last_activity'] = (current_date - df['last_activity']).dt.days

df['Differencial'] = df['Monthly_income'] - df['Monthly_expenses']

df['Payeable'] = (df['Monthly_loan_rate'] < df['Differencial']).astype(int)

df['Approved'] = (
    (df['Differencial'] > 1000) &
    (df['days_since_last_activity'] <= 180) &
    (df['balance'] > 1000) &
    (df['Payeable'] == 1)
).astype(int)

df.to_excel('data_test.xlsx', index=False)
