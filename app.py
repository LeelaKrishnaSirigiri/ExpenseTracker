import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💳",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body{
background-color:#f4f6fb;
}

.header{
font-size:42px;
font-weight:bold;
color:#2c3e50;
text-align:center;
}

.subheader{
font-size:18px;
color:#7f8c8d;
text-align:center;
margin-bottom:30px;
}

.card{
padding:20px;
border-radius:12px;
background:white;
box-shadow:0 6px 15px rgba(0,0,0,0.08);
text-align:center;
}

.metric{
font-size:28px;
font-weight:bold;
color:#2ecc71;
}

.sidebar-logo{
text-align:center;
font-size:26px;
font-weight:bold;
color:#34495e;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- BACKEND CLASS ----------------
class ExpenseTracker:

    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, description):
        expense = {
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        self.expenses.append(expense)

    def total_expense(self):
        return sum(e["Amount"] for e in self.expenses)

    def category_summary(self):
        summary = {}
        for e in self.expenses:
            summary[e["Category"]] = summary.get(e["Category"], 0) + e["Amount"]
        return summary

    def view_expenses(self):
        return self.expenses


# ---------------- SESSION STATE ----------------
if "tracker" not in st.session_state:
    st.session_state.tracker = ExpenseTracker()

tracker = st.session_state.tracker


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("<div class='sidebar-logo'>💰 Expense Tracker</div>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    ["Add Expense", "Dashboard", "All Expenses"]
)


# ---------------- HEADER ----------------
st.markdown("<div class='header'>Personal Expense Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Track your spending and manage your money smarter</div>", unsafe_allow_html=True)


# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    expenses = tracker.view_expenses()

    if len(expenses) == 0:
        st.info("No expenses added yet.")
    else:

        df = pd.DataFrame(expenses)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("Total Spending")
            st.markdown(f"<div class='metric'>₹ {tracker.total_expense()}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("Transactions")
            st.markdown(f"<div class='metric'>{len(df)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("Categories")
            st.markdown(f"<div class='metric'>{df['Category'].nunique()}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


        st.subheader("Category Spending")

        summary = tracker.category_summary()

        chart_df = pd.DataFrame({
            "Category": summary.keys(),
            "Amount": summary.values()
        })

        pie = px.pie(chart_df, names="Category", values="Amount", hole=0.4)
        st.plotly_chart(pie, use_container_width=True)

        st.subheader("Expense Comparison")

        bar = px.bar(chart_df, x="Category", y="Amount", text_auto=True)
        st.plotly_chart(bar, use_container_width=True)


# ---------------- ADD EXPENSE ----------------
elif menu == "Add Expense":

    st.subheader("Add New Expense")

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount", min_value=0.0)

    with col2:
        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
        )

    description = st.text_input("Description")

    if st.button("Add Expense"):
        tracker.add_expense(amount, category, description)
        st.success("Expense added successfully")


# ---------------- VIEW EXPENSES ----------------
elif menu == "All Expenses":

    st.subheader("Expense History")

    expenses = tracker.view_expenses()

    if len(expenses) == 0:
        st.warning("No expenses recorded yet")
    else:
        df = pd.DataFrame(expenses)
        st.dataframe(df, use_container_width=True)