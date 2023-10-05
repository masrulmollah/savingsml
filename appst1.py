import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Function to calculate Total Labor Cost and Expected Cost
def calculate_costs(data):
    data['Total Labor Cost'] = data['Labor Hour per Ton'] * data['Volume (Tons)'] * data['Labor Cost per Hour']
    data['Expected Cost'] = data['Labor Hour per Ton'] * data['Labor Cost per Hour'] * data['Volume Forecast']
    return data

# Function to upload Excel file
def upload_excel():
    st.title("Upload Excel File")
    st.write("Please upload an Excel file with the 'Volume Forecast' data.")

    uploaded_file = st.file_uploader("Choose a file...", type=["xlsx"])

    if uploaded_file is not None:
        new_data = pd.read_excel(uploaded_file)
        new_data = calculate_costs(new_data)

        # Define features (X)
        X = new_data[['Labor Hour per Ton', 'Volume (Tons)', 'Labor Cost per Hour', 'Total Labor Cost', 'Volume Forecast', 'Expected Cost']]

        # Predict using the trained model
        new_predictions = rf_model.predict(X)

        new_data['Predicted Total Labor Cost'] = new_predictions
        new_data['Savings Opportunity'] = new_data['Total Labor Cost'] - new_data['Predicted Total Labor Cost']
        
        positive_savings = new_data[new_data['Savings Opportunity'] > 0]
        st.write("Positive Savings Opportunity:")
        st.write(positive_savings)

# Load the pre-existing data
df = pd.read_excel('main_data.xlsx')
df = calculate_costs(df)

# Define features (X) and target (y)
X = df[['Labor Hour per Ton', 'Volume (Tons)', 'Labor Cost per Hour', 'Total Labor Cost', 'Volume Forecast', 'Expected Cost']]

# Initialize the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X, df['Total Labor Cost'])

# Streamlit app starts here
st.title("Savings Opportunity Calculator")

# Upload Excel file and calculate savings opportunity
upload_excel()
