import pandas as pd

from expense_schemas import (
    ExpenseByCategory,
    ExpenseCreate,
    ExpenseUpdate,
    Expense,
    ExpenseCategory,
    ExpenseSummary,
)

expenses = [
    Expense(
        id=1,
        name="Groceries",
        desc="Weekly groceries",
        amount=150.0,
        category=ExpenseCategory.FOOD,
    ),
    Expense(
        id=2,
        name="Electricity Bill",
        desc="Monthly electricity bill",
        amount=75.0,
        category=ExpenseCategory.UTILITIES,
    ),
    Expense(
        id=3,
        name="Movie Night",
        desc="Cinema tickets",
        amount=30.0,
        category=ExpenseCategory.ENTERTAINMENT,
    ),
]


def load_expenses() -> list[Expense]:
    return expenses


def summary() -> ExpenseSummary:
    expense_count = len(expenses)
    total_expense = sum(expense.amount for expense in expenses)
    highest_expense = max((expense.amount for expense in expenses), default=0)
    average_expense = total_expense / expense_count if expense_count > 0 else 0

    return ExpenseSummary(
        expense_count=expense_count,
        total_expense=total_expense,
        highest_expense=highest_expense,
        average_expense=average_expense,
    )


def get_expenses_by_category() -> list[ExpenseByCategory]:
    return [
        ExpenseByCategory(
            category=category,
            amount=sum(
                expense.amount for expense in expenses if expense.category == category
            ),
        )
        for category in ExpenseCategory
    ]


def get_expense_by_id(expense_id: int) -> Expense | None:
    for expense in load_expenses():
        if expense.id == expense_id:
            return expense
    return None


def add_expense(expense: ExpenseCreate):
    new_id = max(expense.id for expense in expenses) + 1 if expenses else 1
    new_expense = Expense(
        id=new_id,
        name=expense.name,
        desc=expense.desc,
        amount=expense.amount,
        category=expense.category,
    )
    expenses.append(new_expense)


def edit_expense(expense_id: int, expense: ExpenseUpdate):
    for e in expenses:
        if e.id == expense_id:
            for field, value in expense.model_dump(exclude_unset=True).items():
                setattr(e, field, value)
            break


def delete_expense(expense_id: int):
    global expenses
    expenses = [expense for expense in expenses if expense.id != expense_id]
