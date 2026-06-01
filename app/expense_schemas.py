from pydantic import BaseModel, Field
from enum import Enum


class ExpenseCategory(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    OTHER = "other"


class ExpenseCreate(BaseModel):
    name: str = Field(..., min_length=3)
    desc: str | None = None
    amount: float = Field(..., gt=0)
    category: ExpenseCategory


class ExpenseUpdate(BaseModel):
    name: str | None = Field(None, min_length=3)
    desc: str | None = None
    amount: float | None = Field(None, gt=0)
    category: ExpenseCategory | None = None


class Expense(ExpenseCreate):
    id: int


class ExpenseSummary(BaseModel):
    expense_count: int
    total_expense: float
    highest_expense: float
    average_expense: float


class ExpenseByCategory(BaseModel):
    category: ExpenseCategory
    amount: float
