import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="k-Anonymity Anonymizer", layout="wide")

st.title("🛡️ k-Anonymity Data Anonymizer")
st.markdown("*Protect individual privacy while keeping data useful for analysis*")

with st.sidebar:
    st.header("📁 Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    st.header("⚙️ Settings")
    k_value = st.slider("k-anonymity value", min_value=2, max_value=10, value=3)

if uploaded_file is not None:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head(10))
    st.caption(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    st.subheader("🔍 Select Quasi-Identifier Columns")
    st.markdown("*These are columns that could identify a person when combined (e.g., Age, Zip Code, Gender)*")
    
    all_columns = df.columns.tolist()
    quasi_columns = st.multiselect("Choose columns to anonymize", all_columns)
    
    if quasi_columns and st.button("🔒 Anonymize Data", type="primary"):
        with st.spinner("Anonymizing..."):
            df_anon = df.copy()
            
            for col in quasi_columns:
                if df[col].dtype in ['int64', 'float64']:
                    # Numeric: bin into groups
                    n_bins = max(2, len(df[col].unique()) // k_value)
                    df_anon[col] = pd.cut(df[col], bins=n_bins, labels=False)
                else:
                    # Categorical: group rare values
                    value_counts = df[col].value_counts()
                    rare_values = value_counts[value_counts < k_value].index
                    df_anon[col] = df[col].apply(lambda x: 'Other' if x in rare_values else x)
            
            # Compute achieved k-anonymity
            grouped = df_anon[quasi_columns].value_counts()
            min_k = grouped.min()
            
            st.success(f"✅ Anonymization complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Target k-anonymity", k_value)
            with col2:
                st.metric("Achieved k-anonymity", min_k)
                if min_k < k_value:
                    st.warning(f"⚠️ Achieved k ({min_k}) is less than target ({k_value}). Try selecting fewer columns or get more data.")
            
            st.subheader("📊 Anonymized Data Preview")
            st.dataframe(df_anon.head(10))
            
            # Download button
            csv = df_anon.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Anonymized CSV", csv, "anonymized_data.csv", "text/csv")
else:
    st.info("👈 Upload a CSV or Excel file to get started")
    
    with st.expander("📖 What is k-Anonymity?"):
        st.markdown("""
        **k-Anonymity** ensures each person's data cannot be distinguished from at least **k-1** others.
        
        **Example:** A record with Age=25, Zip=12345 appears once → not anonymous.  
        After generalization to Age=20-30, Zip=123** → appears 5 times → k=5 anonymous.
        
        **Real-world use cases:**
        - Hospitals sharing patient data for research
        - Banks sharing transaction patterns
        - Marketing teams analyzing customer segments
        """)

st.markdown("---")
st.caption("🔒 Privacy-preserving data anonymization | Built for production use")
