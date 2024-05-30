import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize the app
st.title("Expense Management for Contracts")

# Add custom CSS to style the transaction type dropdown
st.markdown(
    """
    <style>
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFF00;  /* Yellow background */
        border-radius: 5px;
        padding: 5px;
    }
    .stSelectbox div[data-baseweb="select"] div {
        background-color: #FFFF00;  /* Yellow background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a form for user input
with st.form("expense_form"):
    description = st.text_input("Description")
    transaction_type = st.selectbox("Transaction Type", ["Outflow", "Inflow"], index=0)
    amount = st.number_input("Amount", min_value=0.0, step=0.1)
    comment = st.text_area("Comment")
    submit_button = st.form_submit_button(label="Submit")

# Load existing data
filename = "expenses.csv"
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Description", "Type", "Amount", "Comment"])

# Handle form submission
if submit_button:
    if description and amount > 0:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame([{
            "Date": date,
            "Description": description,
            "Type": transaction_type,
            "Amount": amount,
            "Comment": comment
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)
        st.success("Transaction added successfully!")
    else:
        st.error("Please provide a valid description and amount.")

# Display the data
st.subheader("Transaction History")
st.write(df)

# Calculate and display the net balance
inflows = df[df["Type"] == "Inflow"]["Amount"].sum()
outflows = df[df["Type"] == "Outflow"]["Amount"].sum()
net_balance = inflows - outflows
st.subheader(f"Net Balance: ₹{net_balance:.2f}")
