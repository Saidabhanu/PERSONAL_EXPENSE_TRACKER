# helper.py

# Function to calculate total income
def calculate_income(transactions):

    total_income = 0

    for transaction in transactions:

        if transaction["type"] == "Income":
            total_income += transaction["amount"]

    return total_income


# Function to calculate total expense
def calculate_expense(transactions):

    total_expense = 0

    for transaction in transactions:

        if transaction["type"] == "Expense":
            total_expense += transaction["amount"]

    return total_expense


# Function to calculate balance
def calculate_balance(income, expense):

    balance = income - expense

    return balance