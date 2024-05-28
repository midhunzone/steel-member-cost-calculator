import streamlit as st
import pandas as pd
from datetime import datetime

# Constants
DENSITY_OF_STEEL = 7850  # kg/m^3
MM_TO_METERS = 0.001  # Conversion factor from mm to meters
COST_PER_KG = {
    'Shaft': 70,
    'Plate': 61,
    'Round Plate': 65,
    'Square Angle': 75,
    'C-type Channel': 80,
    'I-joist': 85,
}
TAX_RATE = 0.18  # 18% tax

# Function to calculate weight and cost
def calculate_weight_and_cost(member_type, dimensions, cost_per_kg):
    volume = 0

    if member_type == 'Shaft':
        diameter = dimensions['Diameter'] * MM_TO_METERS
        length = dimensions['Length'] * MM_TO_METERS
        radius = diameter / 2
        volume = 3.1416 * radius ** 2 * length
    elif member_type == 'Plate':
        length = dimensions['Length'] * MM_TO_METERS
        breadth = dimensions['Breadth'] * MM_TO_METERS
        thickness = dimensions['Thickness'] * MM_TO_METERS
        volume = length * breadth * thickness
    elif member_type == 'Round Plate':
        diameter = dimensions['Diameter'] * MM_TO_METERS
        thickness = dimensions['Thickness'] * MM_TO_METERS
        radius = diameter / 2
        volume = 3.1416 * radius ** 2 * thickness
    elif member_type == 'Square Angle':
        length = dimensions['Length'] * MM_TO_METERS
        leg1 = dimensions['Leg 1'] * MM_TO_METERS
        leg2 = dimensions['Leg 2'] * MM_TO_METERS
        thickness = dimensions['Thickness'] * MM_TO_METERS
        volume = length * (leg1 + leg2 - thickness) * thickness
    elif member_type == 'C-type Channel':
        length = dimensions['Length'] * MM_TO_METERS
        web_height = dimensions['Web Height'] * MM_TO_METERS
        flange_width = dimensions['Flange Width'] * MM_TO_METERS
        web_thickness = dimensions['Web Thickness'] * MM_TO_METERS
        flange_thickness = dimensions['Flange Thickness'] * MM_TO_METERS
        volume = length * ((2 * flange_width * flange_thickness) + (web_height - 2 * flange_thickness) * web_thickness)
    elif member_type == 'I-joist':
        length = dimensions['Length'] * MM_TO_METERS
        flange_width = dimensions['Flange Width'] * MM_TO_METERS
        flange_thickness = dimensions['Flange Thickness'] * MM_TO_METERS
        web_height = dimensions['Web Height'] * MM_TO_METERS
        web_thickness = dimensions['Web Thickness'] * MM_TO_METERS
        volume = length * (2 * flange_width * flange_thickness + web_height * web_thickness)

    weight = volume * DENSITY_OF_STEEL
    cost = weight * cost_per_kg
    total_cost = cost + (cost * TAX_RATE)
    return weight, total_cost

# Function to save data to CSV
def save_to_csv(member_type, dimensions, weight, total_cost):
    filename = "orders.csv"
    df = pd.DataFrame(columns=['Date', 'Member Type', 'Dimensions', 'Weight (Kg)', 'Total Cost (Rs)'])

    # Load existing data
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        pass

    # Append new data
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dimensions_str = ", ".join(f"{k}: {v} mm" for k, v in dimensions.items())
    new_data = pd.DataFrame([{'Date': date, 'Member Type': member_type, 'Dimensions': dimensions_str, 'Weight (Kg)': weight, 'Total Cost (Rs)': total_cost}])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save to CSV
    df.to_csv(filename, index=False)

# Streamlit app setup
st.set_page_config(page_title="Steel Member Cost Calculator")

# Run Streamlit app
if __name__ == '__main__':
    menu_options = ["Main Menu", "Calculate Weight and Cost", "View Saved Data"]
    menu_choice = st.sidebar.selectbox("Menu", options=menu_options)

    if menu_choice == "Main Menu":
        st.header("Welcome to the Steel Member Cost Calculator")
        st.write("Please select an option from the menu to proceed.")
    elif menu_choice == "Calculate Weight and Cost":
        member_type = st.selectbox("Select Member Type", options=['Shaft', 'Plate', 'Round Plate', 'Square Angle', 'C-type Channel', 'I-joist'])
        cost_per_kg = st.number_input("Price per Kg (Rs)", value=COST_PER_KG.get(member_type, 0))
        dimensions = {}

        if member_type == 'Shaft':
            dimensions['Diameter'] = st.number_input("Diameter (mm)", min_value=0.0, step=0.1)
            dimensions['Length'] = st.number_input("Length (mm)", min_value=0.0, step=0.1)
        elif member_type == 'Plate':
            dimensions['Length'] = st.number_input("Length (mm)", min_value=0.0, step=0.1)
            dimensions['Breadth'] = st.number_input("Breadth (mm)", min_value=0.0, step=0.1)
            dimensions['Thickness'] = st.number_input("Thickness (mm)", min_value=0.0, step=0.1)
        elif member_type == 'Round Plate':
            dimensions['Diameter'] = st.number_input("Diameter (mm)", min_value=0.0, step=0.1)
            dimensions['Thickness'] = st.number_input("Thickness (mm)", min_value=0.0, step=0.1)
        elif member_type == 'Square Angle':
            dimensions['Length'] = st.number_input("Length (mm)", min_value=0.0, step=0.1)
            dimensions['Leg 1'] = st.number_input("Leg 1 (mm)", min_value=0.0, step=0.1)
            dimensions['Leg 2'] = st.number_input("Leg 2 (mm)", min_value=0.0, step=0.1)
            dimensions['Thickness'] = st.number_input("Thickness (mm)", min_value=0.0, step=0.1)
        elif member_type == 'C-type Channel':
            dimensions['Length'] = st.number_input("Length (mm)", min_value=0.0, step=0.1)
            dimensions['Web Height'] = st.number_input("Web Height (mm)", min_value=0.0, step=0.1)
            dimensions['Flange Width'] = st.number_input("Flange Width (mm)", min_value=0.0, step=0.1)
            dimensions['Web Thickness'] = st.number_input("Web Thickness (mm)", min_value=0.0, step=0.1)
            dimensions['Flange Thickness'] = st.number_input("Flange Thickness (mm)", min_value=0.0, step=0.1)
        elif member_type == 'I-joist':
            dimensions['Length'] = st.number_input("Length (mm)", min_value=0.0, step=0.1)
            dimensions['Flange Width'] = st.number_input("Flange Width (mm)", min_value=0.0, step=0.1)
            dimensions['Flange Thickness'] = st.number_input("Flange Thickness (mm)", min_value=0.0, step=0.1)
            dimensions['Web Height'] = st.number_input("Web Height (mm)", min_value=0.0, step=0.1)
            dimensions['Web Thickness'] = st.number_input("Web Thickness (mm)", min_value=0.0, step=0.1)

        if st.button("Calculate Weight and Cost"):
            if all(dim > 0 for dim in dimensions.values()):
                weight, total_cost = calculate_weight_and_cost(member_type, dimensions, cost_per_kg)
                st.success(f"Weight: {weight:.2f} Kg")
                st.success(f"Total Cost: ₹{total_cost:.2f}")
                save_to_csv(member_type, dimensions, weight, total_cost)
            else:
                st.error("Please enter all dimensions.")
    elif menu_choice == "View Saved Data":
        member_filter = st.selectbox("Filter by Member Type", options=['All', 'Shaft', 'Plate', 'Round Plate', 'Square Angle', 'C-type Channel', 'I-joist'])
        start_date = st.date_input("Start Date", value=datetime.now().date())
        end_date = st.date_input("End Date", value=datetime.now().date())
        filename = "orders.csv"
        try:
            df = pd.read_csv(filename)
            df['Date'] = pd.to_datetime(df['Date'])
            if member_filter != 'All':
                df = df[df['Member Type'] == member_filter]
            df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
            st.write(df)
        except FileNotFoundError:
            st.write("No data available.")
