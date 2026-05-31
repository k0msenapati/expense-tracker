import pandas as pd

categories = ["Food", "Transport", "Entertainment", "Sports", "Other"]

expenses = [
    {
        "id": 1,
        "name": "Lunch",
        "desc": "Office Lunch",
        "amount": 19.55,
        "category": "Food",
    },
    {
        "id": 2,
        "name": "Dinner",
        "desc": "Family Dinner",
        "amount": 50,
        "category": "Food",
    },
    {
        "id": 3,
        "name": "Hockey",
        "desc": "Hockey game with friends",
        "amount": 10,
        "category": "Sports",
    },
]


def load_expenses():
    return expenses


def load_expenses_as_df() -> pd.DataFrame:
    return pd.DataFrame(expenses)


def summary():
    return {
        "expense_count": len(expenses),
        "total_expense": sum(expense["amount"] for expense in expenses),
        "highest_expense": (
            max(expenses, key=lambda x: x["amount"]) if expenses else None
        ),
        "average_expense": (
            sum(expense["amount"] for expense in expenses) / len(expenses)
            if expenses
            else 0
        ),
    }


def get_expenses_by_category():
    return pd.DataFrame(expenses).groupby("category")["amount"].sum().reset_index()


def get_expense_by_id(expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


def add_expense(name, desc, amount, category):
    new_id = max(expense["id"] for expense in expenses) + 1 if expenses else 1
    new_expense = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "amount": amount,
        "category": category,
    }
    expenses.append(new_expense)


def edit_expense(expense_id, name, desc, amount, category):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["name"] = name or expense["name"]
            expense["desc"] = desc or expense["desc"]
            expense["amount"] = amount or expense["amount"]
            expense["category"] = category or expense["category"]
            break


def delete_expense(expense_id):
    global expenses
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
