import streamlit as st
import plotly.express as px

import expense_tracker

st.set_page_config(page_title="Dashboard", page_icon="💸")

st.title("Expense Tracker Dashboard")


def summary_cards():
    st.subheader("Summary")

    summary = expense_tracker.summary()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Expenses", f"${summary['total_expense']:.2f}")

    with col2:
        st.metric("Number of Expenses", summary["expense_count"])

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Highest Expense",
            (
                f"${summary['highest_expense']['amount']:.2f}"
                if summary["highest_expense"]
                else "$0.00"
            ),
        )

    with col4:
        st.metric("Average Expense", f"${summary['average_expense']:.2f}")


def analytics():
    expenses_by_cat = expense_tracker.get_expenses_by_category()

    st.subheader("Expenses by Categories")

    fig = px.pie(expenses_by_cat, names="category", values="amount")
    st.plotly_chart(fig)


def expense_list():
    st.subheader("Expenses")

    expenses = expense_tracker.load_expenses_as_df()

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("Search")

    with col2:
        category_filter = st.selectbox("Category", ["All"] + expense_tracker.categories)

    # Search filter
    if search:
        expenses = expenses[
            expenses["name"].str.contains(search, case=False, na=False)
            | expenses["desc"].str.contains(search, case=False, na=False)
        ]

    # Category filter
    if category_filter != "All":
        expenses = expenses[expenses["category"] == category_filter]

    st.dataframe(expenses, width="stretch")

    expense_delete()

    expense_export(expenses)


def expense_delete():
    col1, col2 = st.columns([4, 1])

    with col1:
        selected_expense = st.selectbox(
            "Select Expense",
            options=expense_tracker.load_expenses(),
            format_func=lambda x: f"{x['id']} - {x['desc']} - ${x['amount']:.2f}",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("🗑️ Delete"):
            expense_tracker.delete_expense(selected_expense["id"])
            st.rerun()


def expense_export(expenses):
    st.download_button(
        "Export Data",
        data=expenses.to_csv(index=False),
        file_name="expenses.csv",
        mime="text/csv",
    )

def dashboard():
    summary_cards()
    analytics()
    expense_list()

if __name__ == "__main__":
    dashboard()
