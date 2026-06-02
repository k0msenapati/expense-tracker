from sqlmodel import SQLModel, Field


class Expense(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    
    id: int | None = Field(default=None, primary_key=True)

    name: str
    desc: str | None = None
    amount: float
    category: str
