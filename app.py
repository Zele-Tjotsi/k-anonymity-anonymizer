import streamlit as st
import pandas as pd
import numpy as np
from privacy_metrics import compute_l_diversity, check_l_diversity_threshold

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
            
            st.success("Anonymization complete")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Target k-anonymity", k_value)
            with col2:
                st.metric("Achieved k-anonymity", min_k)
                if min_k < k_value:
                    st.warning(f"Achieved k ({min_k}) is less than target ({k_value}). Try selecting fewer columns or increasing data size.")
            
            # Advanced Privacy Metrics Section
            st.subheader("Advanced Privacy Analysis")
            
            # Ask user if they want l-diversity analysis
            with st.expander("l-Diversity Analysis (Extended Privacy)"):
                st.markdown("""
                **What is l-diversity?**  
                k-anonymity hides identity but not sensitive information. l-diversity ensures each group has at least `l` distinct values for sensitive attributes.
                
                **Example:** If all 50 people in a k-anonymous group have "HIV" as disease, privacy is still violated. l-diversity prevents this.
                """)
                
                # Let user select a sensitive column
                all_columns = df.columns.tolist()
                sensitive_column = st.selectbox(
                    "Select a sensitive column to analyze (e.g., Disease, Salary, Diagnosis)",
                    ["None"] + all_columns,
                    help="This column contains the sensitive information you want to protect (e.g., medical conditions, income)"
                )
                
                if sensitive_column != "None" and quasi_columns:
                    l_diversity_result = compute_l_diversity(df_anon, quasi_columns, sensitive_column)
                    
                    if "error" in l_diversity_result:
                        st.error(l_diversity_result["error"])
                    else:
                        st.metric("Minimum l-diversity", l_diversity_result["min_l_diversity"])
                        st.metric("Average l-diversity", l_diversity_result["avg_l_diversity"])
                        
                        # Interpret the result
                        if l_diversity_result["min_l_diversity"] >= 3:
                            st.success("Strong l-diversity: Each group has at least 3 distinct sensitive values.")
                        elif l_diversity_result["min_l_diversity"] >= 2:
                            st.info("Moderate l-diversity: Some groups have only 2 distinct values. May be acceptable for many use cases.")
                        else:
                            st.warning(f"Low l-diversity: {l_diversity_result['groups_below_threshold']} out of {l_diversity_result['total_groups']} groups have only 1 distinct sensitive value. Attribute disclosure possible.")
                        
                        # Show interpretation
                        st.caption(l_diversity_result["interpretation"])
                        
                        # Optional: Show detailed breakdown
                        with st.expander("View detailed breakdown by group"):
                            for group_key, details in list(l_diversity_result["details"].items())[:5]:  # Show first 5 groups
                                st.markdown(f"**Group {group_key}**")
                                st.write(f"- Size: {details['size']} records")
                                st.write(f"- Diversity: {details['diversity']} unique values")
                                st.write(f"- Distinct values: {', '.join(str(v) for v in details['unique_values'][:3])}...")
                                st.divider()
                elif sensitive_column != "None" and not quasi_columns:
                    st.info("Select quasi-identifier columns first to enable l-diversity analysis.")
            
            st.subheader("Anonymized Data Preview")
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
