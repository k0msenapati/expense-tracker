import streamlit as st

import expense_tracker

st.set_page_config(page_title="Edit Expense", page_icon="💸")

st.title("Edit Expense")

expense = st.selectbox(
    "Select Expense to Edit",
    options=expense_tracker.load_expenses(),
    format_func=lambda x: f"{x['name']} - ${x['amount']:.2f} ({x['category']})",
)

with st.form("edit_expense_form"):
    name = st.text_input("Expense Name", value=expense["name"])
    desc = st.text_area("Description", value=expense["desc"])
    amount = st.number_input(
        "Amount", min_value=0.0, step=1.0, value=float(expense["amount"])
    )
    category = st.selectbox(
        "Category",
        expense_tracker.categories,
        index=expense_tracker.categories.index(expense["category"]),
    )

    submitted = st.form_submit_button("Edit Expense")

    if submitted:
        expense_tracker.edit_expense(expense["id"], name, desc, amount, category)
        st.success(f"Edited expense: {name} - ${amount:.2f} in category {category}")
        st.switch_page("📊_dashboard.py")
