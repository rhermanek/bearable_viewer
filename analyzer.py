import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    symptom_scores = symptom_data.groupby(['date formatted', 'symptom_type'])['rating/amount'].sum().unstack(fill_value=0)
    
    # Dynamically get a list of symptoms in the file
    all_symptoms = list(symptom_scores.columns)
    
    # Step 3: User selects symptoms to display
    st.sidebar.header("Select Symptoms to Display")
    selected_symptoms = []
    for symptom in all_symptoms:
        if st.sidebar.checkbox(symptom, value=True):  # Default to checked
            selected_symptoms.append(symptom)
    
    # Filter the symptom data based on selections
    symptom_scores_filtered = symptom_scores[selected_symptoms]
    
    # Step 4: Plot the data
    st.subheader("Symptom Score Over Time")
    
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    
    # Plot each selected symptom type individually with markers for clarity
    for symptom_type in symptom_scores_filtered.columns:
        symptom_scores_filtered[symptom_type].plot(
            kind='line',
            ax=ax,
            marker='o',
            linestyle='-',
            linewidth=1.5,
            label=symptom_type
        )
    
    plt.title("Symptom Score Over Time by Selected Symptom Types")
    plt.xlabel("Date")
    plt.ylabel("Symptom Score")
    plt.legend(title='Symptom Type', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    
    st.pyplot(plt)
else:
    st.write("Please upload a CSV file to see the analysis.")
