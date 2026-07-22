import streamlit as st
import pandas as pd
import numpy as np


def show_data_cleaning_ai(df):

    st.markdown("---")
    st.subheader("🧹 AI Data Cleaning Assistant")

    if df is None:
        st.warning("Upload dataset first.")
        return

    missing = df.isnull().sum()

    duplicates = df.duplicated().sum()

    numeric = df.select_dtypes(include=np.number)

    outliers = 0

    for col in numeric.columns:

        Q1 = numeric[col].quantile(0.25)
        Q3 = numeric[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers += ((numeric[col] < lower) | (numeric[col] > upper)).sum()

    score = 100

    score -= missing.sum() * 0.5
    score -= duplicates * 2
    score -= outliers * 0.2

    score = max(0, round(score, 2))

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Health Score", f"{score}/100")
    c2.metric("Missing Values", int(missing.sum()))
    c3.metric("Duplicate Rows", int(duplicates))
    c4.metric("Outliers", int(outliers))

    st.markdown("## Missing Values")

    st.dataframe(missing.reset_index().rename(
        columns={
            "index": "Column",
            0: "Missing"
        }
    ))

    st.markdown("## AI Suggestions")

    if missing.sum() > 0:
        st.warning("✔ Fill Missing Values")

    if duplicates > 0:
        st.warning("✔ Remove Duplicate Rows")

    if outliers > 0:
        st.warning("✔ Review Outliers")

    if missing.sum() == 0 and duplicates == 0 and outliers == 0:
        st.success("Dataset looks clean.")