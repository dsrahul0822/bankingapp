import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid

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

def save_customers(df):
    df.to_csv(CUSTOMER_FILE, index=False)

def add_transaction(account_number, amount):
    df_txn = load_transactions()
    transaction_id = str(uuid.uuid4())[:8]
    new_txn = pd.DataFrame([{
        "transaction_id": transaction_id,
        "account_number": account_number,
        "type": "withdraw",
        "amount": amount,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    updated_df = pd.concat([df_txn, new_txn], ignore_index=True)
    updated_df.to_csv(TRANSACTION_FILE, index=False)

# Page config
st.set_page_config(page_title="Withdraw Money (Admin)", layout="centered")
st.title("🏧 Admin - Withdraw Money")

# Restrict to Admin only
if not st.session_state.get("logged_in") or not st.session_state.get("is_admin"):
    st.error("❌ Access Denied. Only Admins can perform withdrawals.")
    st.stop()

# Select customer
df = load_customers()
if df.empty:
    st.warning("⚠️ No customers found.")
    st.stop()

customer_list = df['account_number'].astype(str) + " - " + df['name']
selected_customer = st.selectbox("Select Customer", customer_list)
account_number = int(selected_customer.split(" - ")[0])

# Get customer balance
idx = df[df['account_number'] == account_number].index[0]
current_balance = df.at[idx, 'balance']
st.info(f"💼 Current Balance for Account {account_number}: ₹{current_balance}")

# Withdrawal amount input
amount = st.number_input("Enter amount to withdraw", min_value=1, step=100)

if st.button("Withdraw"):
    if amount > current_balance:
        st.warning("⚠️ Insufficient balance.")
    else:
        df.at[idx, 'balance'] -= amount
        save_customers(df)
        add_transaction(account_number, amount)
        st.success(f"✅ ₹{amount} withdrawn from Account {account_number}")
        st.info(f"💼 New Balance: ₹{df.at[idx, 'balance']}")
