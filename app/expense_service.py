from sqlmodel import select

from database import get_session, Session
from expense_model import Expense as ExpenseModel
from expense_schemas import (
    ExpenseByCategory,
    ExpenseCreate,
    ExpenseUpdate,
    Expense,
    ExpenseCategory,
    ExpenseSummary,
)


def load_expenses() -> list[Expense]:
    with get_session() as session:
        statement = select(ExpenseModel)
        results = session.exec(statement).all()

        expenses = []
        for expense in results:
            assert expense.id is not None

            expenses.append(
                Expense(
                    id=expense.id,
                    name=expense.name,
                    desc=expense.desc,
                    amount=expense.amount,
                    category=ExpenseCategory(expense.category),
                )
            )

        return expenses


def summary() -> ExpenseSummary:
    expenses = load_expenses()

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
    expenses = load_expenses()

    return [
        ExpenseByCategory(
            category=category,
            amount=sum(
                expense.amount for expense in expenses if expense.category == category
            ),
        )
        for category in ExpenseCategory
    ]


def get_expense_by_id(session: Session, expense_id: int) -> ExpenseModel | None:
    statement = select(ExpenseModel).where(ExpenseModel.id == expense_id)
    result = session.exec(statement).first()

    return result


def add_expense(expense: ExpenseCreate):
    with get_session() as session:
        new_expense = ExpenseModel(
            name=expense.name,
            desc=expense.desc,
            amount=expense.amount,
            category=expense.category.value,
        )
        session.add(new_expense)
        session.commit()


def edit_expense(expense_id: int, data: ExpenseUpdate):
    with get_session() as session:
        expense = get_expense_by_id(session, expense_id)

        if expense is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, ExpenseCategory):
                value = value.value

            setattr(expense, field, value)

        session.commit()
        session.refresh(expense)

        assert expense.id is not None

        return Expense(
            id=expense.id,
            name=expense.name,
            desc=expense.desc,
            amount=expense.amount,
            category=ExpenseCategory(expense.category),
        )


def delete_expense(expense_id: int):
    with get_session() as session:
        expense = get_expense_by_id(session, expense_id)

        if expense is None:
            return False

        session.delete(expense)
        session.commit()
        return True
