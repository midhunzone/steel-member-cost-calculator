Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st
... import pandas as pd
... from datetime import datetime
... 
... # Function to load existing data
... def load_data(file):
...     try:
...         return pd.read_csv(file)
...     except FileNotFoundError:
...         return pd.DataFrame(columns=['Date', 'Description', 'Inflow', 'Outflow', 'Comments'])
... 
... # Function to save data to CSV
... def save_data(file, data):
...     data.to_csv(file, index=False)
... 
... # Initialize file path
... file_path = 'expense_data.csv'
... 
... # Load existing data
... data = load_data(file_path)
... 
... # Streamlit UI
... st.title("Contract Expense Management")
... 
... st.subheader("Add New Entry")
... description = st.text_input("Description")
... inflow = st.number_input("Inflow (Funds Received)", min_value=0.0, step=0.01)
... outflow = st.number_input("Outflow (Expenses)", min_value=0.0, step=0.01)
... comments = st.text_area("Comments")
... 
... if st.button("Add Entry"):
...     if description:
...         new_entry = pd.DataFrame([{
...             'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
...             'Description': description,
...             'Inflow': inflow,
            'Outflow': outflow,
            'Comments': comments
        }])
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(file_path, data)
        st.success("Entry added successfully!")
    else:
        st.error("Description is required to add an entry.")

st.subheader("All Entries")
if not data.empty:
    st.dataframe(data)
else:
    st.write("No data available.")

# Calculate and display net balance
total_inflow = data['Inflow'].sum()
total_outflow = data['Outflow'].sum()
net_balance = total_inflow - total_outflow

st.subheader("Summary")
st.write(f"Total Inflow: ₹{total_inflow:.2f}")
st.write(f"Total Outflow: ₹{total_outflow:.2f}")
st.write(f"Net Balance: ₹{net_balance:.2f}")

# Option to download the data
st.download_button(
    label="Download Data as CSV",
    data=data.to_csv(index=False),
    file_name='expense_data.csv',
    mime='text/csv'
)
