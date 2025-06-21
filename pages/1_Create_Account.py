import streamlit as st
import pandas as pd
import os
import random

CUSTOMER_FILE = "data/customers.csv"

# Ensure customer file exists
if not os.path.exists(CUSTOMER_FILE):
    df_empty = pd.DataFrame(columns=["account_number", "name", "password", "balance"])
    df_empty.to_csv(CUSTOMER_FILE, index=False)

# Load existing customers
def load_customers():
    return pd.read_csv(CUSTOMER_FILE)

# Save new customer
def save_customer(name, password, balance):
    df = load_customers()

    # Generate unique account number
    while True:
        account_number = random.randint(1000, 9999)
        if account_number not in df['account_number'].values:
            break

    new_customer = pd.DataFrame([{
        "account_number": account_number,
        "name": name,
        "password": password,
        "balance": balance
    }])

    updated_df = pd.concat([df, new_customer], ignore_index=True)
    updated_df.to_csv(CUSTOMER_FILE, index=False)

    return account_number

# Only Admin can access this page
if not st.session_state.get("is_admin"):
    st.error("❌ Access Denied. Only Admins can create new accounts.")
    st.stop()

st.set_page_config(page_title="Create Account", layout="centered")
st.title("👤 Create New Bank Account")

with st.form("create_account_form"):
    name = st.text_input("Customer Name")
    password = st.text_input("Set Password", type="password")
    balance = st.number_input("Initial Balance", min_value=0, step=100)

    submitted = st.form_submit_button("Create Account")

    if submitted:
        if name.strip() == "" or password.strip() == "":
            st.warning("Please fill in all fields.")
        else:
            account_number = save_customer(name, password, balance)
            st.success(f"✅ Account created successfully! Account Number: {account_number}")
