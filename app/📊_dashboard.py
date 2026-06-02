import streamlit as st
import pandas as pd
import plotly.express as px

from expense_schemas import ExpenseCategory
from database import create_db
import expense_service

if "db_initialized" not in st.session_state:
    create_db()
    st.session_state["db_initialized"] = True

st.set_page_config(page_title="Dashboard", page_icon="💸")

st.title("Expense Tracker Dashboard")


def load_expenses_as_df():
    expenses = expense_service.load_expenses()
    if len(expenses) == 0:
        return pd.DataFrame()

    df = pd.DataFrame([expense.model_dump() for expense in expenses])
    df["category"] = df["category"].apply(lambda c: c.value)
    return df


def summary_cards():
    st.subheader("Summary")

    summary = expense_service.summary()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Expenses", f"${summary.total_expense:.2f}")

    with col2:
        st.metric("Number of Expenses", summary.expense_count)

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Highest Expense",
            (f"${summary.highest_expense:.2f}" if summary.highest_expense else "$0.00"),
        )

    with col4:
        st.metric("Average Expense", f"${summary.average_expense:.2f}")


def analytics():
    expenses_by_cat = expense_service.get_expenses_by_category()

    df = pd.DataFrame([expense.model_dump() for expense in expenses_by_cat])
    df["category"] = df["category"].apply(lambda c: c.value)

    st.subheader("Expenses by Categories")

    fig = px.pie(df, names="category", values="amount")
    st.plotly_chart(fig)


def expense_list():
    st.subheader("Expenses")

    df = load_expenses_as_df()

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("Search")

    with col2:
        category_filter = st.selectbox(
            "Category",
            options=["All", *[cat.value for cat in ExpenseCategory]],
        )

    # Search filter
    if search:
        df = df[
            df["name"].str.contains(search, case=False, na=False)
            | df["desc"].str.contains(search, case=False, na=False)
        ]

    # Category filter
    if category_filter != "All":
        df = df[df["category"] == category_filter]

    st.dataframe(df, width="stretch")

    expense_delete()

    expense_export(df)


def expense_delete():
    col1, col2 = st.columns([4, 1])

    with col1:
        selected_expense = st.selectbox(
            "Select Expense",
            options=expense_service.load_expenses(),
            format_func=lambda x: f"{x.id} - {x.desc} - ${x.amount:.2f}",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("🗑️ Delete"):
            expense_service.delete_expense(selected_expense.id)
            st.rerun()


def expense_export(expenses):
    st.download_button(
        "Export Data",
        data=expenses.to_csv(index=False),
        file_name="expenses.csv",
        mime="text/csv",
    )


def dashboard():
    df = load_expenses_as_df()
    if df.empty:
        st.info("No expenses found. Please add some expenses to see the dashboard.")
        if st.button("Add Expense"):
            st.switch_page("pages/2_➕_add_expense.py")
        return

    summary_cards()
    analytics()
    expense_list()


if __name__ == "__main__":
    dashboard()
