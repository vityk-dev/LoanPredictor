import joblib
import pandas as pd

model = joblib.load('trained_model.pkl')

class User:
    def __init__(self, name, balance, days_since_last_activity, monthly_income, monthly_expenses, monthly_loan_rate):
        self.name = name.upper()
        self.balance = balance
        self.days_since_last_activity = days_since_last_activity
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.monthly_loan_rate = monthly_loan_rate
        self.differencial = self.monthly_income - self.monthly_expenses
        self.payeable = 1 if self.differencial > self.monthly_loan_rate else 0

    def to_dict(self):
        return {
            "Balance": self.balance,
            "Days Since Last Activity": self.days_since_last_activity,
            "Monthly Income": self.monthly_income,
            "Monthly Expenses": self.monthly_expenses,
            "Monthly Loan Rate": self.monthly_loan_rate,
            "Differencial": self.differencial
        }

class LoanApprovalSystem:
    def __init__(self, model):
        self.model = model
        self.dataset_approved = {}

    def predict_decision(self, user):
        input_data = pd.DataFrame({
            'Payeable': [user.payeable],
            'balance': [user.balance],
            'days_since_last_activity': [user.days_since_last_activity],
            'Differencial': [user.differencial]
        })

        prediction = self.model.predict(input_data)
        
        if prediction[0] == 1:
            print("The decision is: Approved")
            # add user to the approved dataset
            self.dataset_approved[user.name] = user.to_dict()
        else:
            print("The decision is: Not Approved")

    def display_approved_users(self):
        print("\nDataset of Approved People:")
        for name, data in self.dataset_approved.items():
            print(f"{name}: {data}")


def main():
    system = LoanApprovalSystem(model)

    print("Please provide the following information:")
    name = input("Name: ")
    balance = float(input("Balance (at the moment): "))
    days_since_last_activity = int(input("Days since last activity: "))
    monthly_income = float(input("Monthly income (in dollars): "))
    monthly_expenses = float(input("Monthly expenses (in dollars): "))
    monthly_loan_rate = float(input("Monthly loan rate (in dollars): "))

    user = User(name, balance, days_since_last_activity, monthly_income, monthly_expenses, monthly_loan_rate)

    system.predict_decision(user)

    # approved users
    system.display_approved_users()


main()