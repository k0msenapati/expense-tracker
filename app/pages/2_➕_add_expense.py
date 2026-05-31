import streamlit as st

import expense_tracker

st.set_page_config(page_title="Add Expense", page_icon="💸")

st.title("Add Expense")

with st.form("add_expense_form"):
    name = st.text_input("Expense Name")
    desc = st.text_area("Description")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.selectbox("Category", expense_tracker.categories)

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        expense_tracker.add_expense(name, desc, amount, category)
        st.success(f"Added expense: {name} - ${amount:.2f} in category {category}")
        st.switch_page("📊_dashboard.py")
