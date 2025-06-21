import streamlit as st
import pandas as pd
import os

CUSTOMER_FILE = "data/customers.csv"

# Ensure customer file exists
if not os.path.exists(CUSTOMER_FILE):
    df_empty = pd.DataFrame(columns=["account_number", "name", "password", "balance"])
    df_empty.to_csv(CUSTOMER_FILE, index=False)

# Read customer data
def load_customers():
    return pd.read_csv(CUSTOMER_FILE)

def authenticate(account_number, password):
    df = load_customers()
    user = df[(df['account_number'] == int(account_number)) & (df['password'] == password)]
    return not user.empty

# Streamlit config
st.set_page_config(page_title="Banking App Login", layout="centered")
st.title("🏦 Welcome to MyBank")
st.subheader("🔐 Login to continue")

login_type = st.radio("Login as", ["Customer", "Admin"])

if login_type == "Admin":
    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if admin_user == "admin" and admin_pass == "admin123":
            st.success("✅ Admin login successful!")
            st.session_state['is_admin'] = True
            st.session_state['logged_in'] = True
            st.session_state['account_number'] = None
            st.info("Go to **Page 1: Create Account** to add new customers.")
        else:
            st.error("❌ Invalid Admin credentials.")

else:
    account_number = st.text_input("Account Number")
    password = st.text_input("Password", type="password")

    if st.button("Login as Customer"):
        if account_number.strip() == "" or password.strip() == "":
            st.warning("Please fill in both fields.")
        else:
            if authenticate(account_number, password):
                st.success("✅ Login successful!")
                st.session_state['logged_in'] = True
                st.session_state['account_number'] = int(account_number)
            else:
                st.error("❌ Invalid account number or password.")

# Optional debug
# st.write(st.session_state)
