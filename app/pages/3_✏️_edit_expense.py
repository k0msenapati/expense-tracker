import streamlit as st

from expense_service import edit_expense, load_expenses
from expense_schemas import ExpenseUpdate, ExpenseCategory

st.set_page_config(page_title="Edit Expense", page_icon="💸")

st.title("Edit Expense")

expense = st.selectbox(
    "Select Expense to Edit",
    options=load_expenses(),
    format_func=lambda x: f"{x.name} - ${x.amount:.2f} ({x.category})",
)

with st.form("edit_expense_form"):
    name = st.text_input("Expense Name", value=expense.name)
    desc = st.text_area("Description", value=expense.desc)
    amount = st.number_input(
        "Amount", min_value=0.0, step=1.0, value=float(expense.amount)
    )
    category = st.selectbox(
        "Category",
        options=list(ExpenseCategory),
        format_func=lambda c: c.value,
    )

    submitted = st.form_submit_button("Edit Expense")

    if submitted:
        new_expense = ExpenseUpdate(
            name=name, desc=desc, amount=amount, category=category
        )
        edit_expense(expense.id, new_expense)

        st.success(f"Edited expense: {name} - ${amount:.2f} in category {category}")
        st.switch_page("📊_dashboard.py")
