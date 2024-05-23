Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st
... import pandas as pd
... from datetime import datetime
... 
... # Load or create new DataFrame
... csv_file = 'purchase_data.csv'
... try:
...     df = pd.read_csv(csv_file)
... except FileNotFoundError:
...     df = pd.DataFrame(columns=["Description", "Specification", "Quantity", "Unit of Measurement", "Date of Entry"])
... 
... # Form to add new data
... with st.form("my_form"):
...     description = st.text_input("Description")
...     specification = st.text_input("Specification")
...     quantity = st.number_input("Quantity", min_value=1, format='%d')
...     unit_of_measurement = st.selectbox("Unit of Measurement", ["Nos", "Kg", "Litres"])
...     submitted = st.form_submit_button("Submit")
... 
...     if submitted:
...         new_data = {"Description": description, "Specification": specification, "Quantity": quantity, "Unit of Measurement": unit_of_measurement, "Date of Entry": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
...         df = df.append(new_data, ignore_index=True)
...         df.to_csv(csv_file, index=False)
... 
... # Display the DataFrame
... st.write(df)
