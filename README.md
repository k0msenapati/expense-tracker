# Expense Tracker 💸

A simple expense tracking app built with Python and Streamlit.


## Features

- Dashboard with total expenses, average spending, highest expense, and transaction count.
- Pie chart visualization of expenses by category.
- Add, view, edit, and delete expenses.
- Search and filter transactions.
- Export expense data to CSV.
- Local SQLite database for persistent storage.


## 🛠️ Tech Stack

- **Core**: [Python 3.13+](https://www.python.org/)
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Visualization**: [Plotly](https://plotly.com/python/)
- **Package Management**: [uv](https://github.com/astral-sh/uv)


## 🚀 Installation & Usage

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/k0msenapati/expense-tracker.git
   cd expense-tracker
   ```

2. **Sync dependencies**:
   ```bash
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run streamlit run app/📊_dashboard.py
   ```

4. **Access the app**:
   Open your browser and navigate to `http://localhost:8501` to start tracking your expenses!

