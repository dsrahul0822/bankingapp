import streamlit as st
import pandas as pd
import os

CUSTOMER_FILE = "data/customers.csv"
TRANSACTION_FILE = "data/transactions.csv"

# Ensure files exist
if not os.path.exists(CUSTOMER_FILE):
    pd.DataFrame(columns=["account_number", "name", "password", "balance"]).to_csv(CUSTOMER_FILE, index=False)

if not os.path.exists(TRANSACTION_FILE):
    pd.DataFrame(columns=["transaction_id", "account_number", "type", "amount", "date_time"]).to_csv(TRANSACTION_FILE, index=False)

def load_customers():
    return pd.read_csv(CUSTOMER_FILE)

def load_transactions():
    return pd.read_csv(TRANSACTION_FILE)

# Page config
st.set_page_config(page_title="Bank Statement", layout="centered")
st.title("📄 Bank Statement")

# Restrict to Admin only
if not st.session_state.get("logged_in") or not st.session_state.get("is_admin"):
    st.error("❌ Access Denied. Only Admins can view bank statements.")
    st.stop()

# Load data
df_customers = load_customers()
df_transactions = load_transactions()

if df_customers.empty:
    st.warning("⚠️ No customers available.")
    st.stop()

# Select customer
customer_list = df_customers['account_number'].astype(str) + " - " + df_customers['name']
selected_customer = st.selectbox("Select Customer", customer_list)
account_number = int(selected_customer.split(" - ")[0])

# Show balance
cust_row = df_customers[df_customers['account_number'] == account_number]
balance = cust_row.iloc[0]['balance']
st.info(f"💼 Current Balance: ₹{balance}")

# Filter transactions
cust_txns = df_transactions[df_transactions['account_number'] == account_number]

if cust_txns.empty:
    st.warning("ℹ️ No transactions available for this customer.")
else:
    st.subheader("📑 Transaction History")
    st.dataframe(cust_txns.sort_values(by="date_time", ascending=False), use_container_width=True)
