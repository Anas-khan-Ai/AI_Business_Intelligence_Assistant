import streamlit as st
import pandas as pd
import numpy as np


def show_preprocessing(df):

    st.markdown("---")
    st.subheader("🧹 Data Preprocessing")

    if df is None:
        st.warning("Please upload a dataset first.")
        return df

    st.write("### Dataset Quality Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", len(df))

    with col2:
        st.metric("Columns", len(df.columns))

    with col3:
        st.metric("Duplicates", df.duplicated().sum())

    st.write("### Missing Values")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        st.success("✅ No Missing Values Found")
    else:
        st.dataframe(missing)

    if st.button("Clean Dataset"):

        clean_df = df.copy()

        # Remove duplicates
        clean_df = clean_df.drop_duplicates()

        # Fill numeric columns
        numeric_cols = clean_df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            clean_df[col] = clean_df[col].fillna(clean_df[col].median())

        # Fill categorical columns
        cat_cols = clean_df.select_dtypes(include="object").columns

        for col in cat_cols:
            clean_df[col] = clean_df[col].fillna(clean_df[col].mode()[0])

        st.success("✅ Dataset Cleaned Successfully")

        st.write("### Clean Dataset Preview")

        st.dataframe(clean_df.head())

        csv = clean_df.to_csv(index=False)

        st.download_button(
            "📥 Download Clean Dataset",
            csv,
            file_name="clean_dataset.csv",
            mime="text/csv"
        )

        return clean_df

    return df