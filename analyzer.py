import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Symptom Analysis Dashboard")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Step 2: Read and process CSV
    data = pd.read_csv(uploaded_file)
    data['date formatted'] = pd.to_datetime(data['date formatted'], errors='coerce')
    
    # Filter for category "Symptom"
    symptom_data = data[data['category'] == 'Symptom']
    
    # Convert 'rating/amount' to numeric
    symptom_data['rating/amount'] = pd.to_numeric(symptom_data['rating/amount'], errors='coerce')
    
    # Extract symptom type from 'detail' column
    symptom_data['symptom_type'] = symptom_data['detail'].str.extract(r'([a-zA-Z]+)')[0]
    
    # Group by date and symptom type, summing the 'rating/amount'
    symptom_scores = symptom_data.groupby(['date formatted', 'symptom_type'])['rating/amount'].sum().reset_index()
    
    # Dynamically get a list of symptoms in the file
    all_symptoms = symptom_scores['symptom_type'].unique()
    
    # Step 3: User selects symptoms to display
    st.sidebar.header("Select Symptoms to Display")
    selected_symptoms = st.sidebar.multiselect("Symptoms", options=all_symptoms, default=list(all_symptoms))
    
    # Filter the data based on selected symptoms
    symptom_scores_filtered = symptom_scores[symptom_scores['symptom_type'].isin(selected_symptoms)]
    
    # Step 4: Plot the data using Plotly
    st.subheader("Symptom Score Over Time")
    
    # Plotly line chart
    fig = px.line(
        symptom_scores_filtered, 
        x="date formatted", 
        y="rating/amount", 
        color="symptom_type",
        title="Symptom Score Over Time by Selected Symptom Types",
        labels={"date formatted": "Date", "rating/amount": "Symptom Score"},
    )
    
    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("Please upload a CSV file to see the analysis.")
