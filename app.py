# app.py

import streamlit as st
import pandas as pd
from datetime import datetime

# Import helper functions
from helper import (
    calculate_income,
    calculate_expense,
    calculate_balance
)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Personal Expense Tracker",
    layout="wide"
)

# -------------------------------
# Session State
# -------------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":

    st.title("💰 Personal Expense Tracker")

    st.write("""
    This application helps users manage
    their income and expenses easily.
    """)

    st.subheader("🎯 Features")

    st.write("""
    - Add Income
    - Add Expenses
    - View Transactions
    - Calculate Balance
    - Category-wise Expense Summary
    """)

# -------------------------------
# Add Transaction
# -------------------------------
elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Select Type",
        ["Income", "Expense"]
    )

    # Categories
    income_categories = [
        "Salary",
        "Business",
        "Freelancing",
        "Bonus",
        "Other"
    ]

    expense_categories = [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Education",
        "Medical",
        "Others"
    ]

    # Category Selection
    if transaction_type == "Income":
        category = st.selectbox(
            "Income Source",
            income_categories
        )

    else:
        category = st.selectbox(
            "Expense Category",
            expense_categories
        )

    # Amount
    amount = st.number_input(
        "Enter Amount",
        min_value=0.0,
        format="%.2f"
    )

    # Date
    date = st.date_input(
        "Select Date",
        datetime.today()
    )

    # Description
    description = st.text_area(
        "Description"
    )

    # Button
    if st.button("Add Transaction"):

        if amount > 0:

            transaction = {
                "type": transaction_type,
                "category": category,
                "amount": amount,
                "date": date.strftime("%d-%m-%Y"),
                "description": description
            }

            st.session_state.transactions.append(
                transaction
            )

            st.success(
                "✅ Transaction Added Successfully!"
            )

        else:
            st.error(
                "❌ Please Enter Valid Amount"
            )

# -------------------------------
# View Transactions
# -------------------------------
elif page == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(
            st.session_state.transactions
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info("No Transactions Available")

# -------------------------------
# Summary Page
# -------------------------------
elif page == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        # Convert to DataFrame
        df = pd.DataFrame(
            st.session_state.transactions
        )

        # Calculations using helpers
        total_income = calculate_income(
            st.session_state.transactions
        )

        total_expense = calculate_expense(
            st.session_state.transactions
        )

        balance = calculate_balance(
            total_income,
            total_expense
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💵 Total Income",
                f"₹ {total_income}"
            )

        with col2:
            st.metric(
                "💸 Total Expense",
                f"₹ {total_expense}"
            )

        with col3:
            st.metric(
                "🏦 Balance",
                f"₹ {balance}"
            )

        # ---------------------------
        # Category-wise Summary
        # ---------------------------
        st.subheader(
            "📌 Category-wise Expense Summary"
        )

        expense_df = df[
            df["type"] == "Expense"
        ]

        if not expense_df.empty:

            category_summary = (
                expense_df.groupby("category")
                ["amount"]
                .sum()
                .reset_index()
            )

            category_summary.columns = [
                "Category",
                "Total Spent (₹)"
            ]

            st.table(category_summary)

        else:
            st.info("No Expense Data Available")

    else:
        st.warning("No Transactions Added Yet")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")

st.caption(
    "Personal Expense Tracker using Python & Streamlit"
)