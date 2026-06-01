import streamlit as st

from expense_service import add_expense
from expense_schemas import ExpenseCreate, ExpenseCategory

st.set_page_config(page_title="Add Expense", page_icon="💸")

st.title("Add Expense")

with st.form("add_expense_form"):
    name = st.text_input("Expense Name")
    desc = st.text_area("Description")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.selectbox(
        "Category",
        options=list(ExpenseCategory),
        format_func=lambda c: c.value,
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = ExpenseCreate(
            name=name, desc=desc, amount=amount, category=category
        )
        add_expense(new_expense)
        
        st.success(f"Added expense: {name} - ${amount:.2f} in category {category}")
        st.switch_page("📊_dashboard.py")
