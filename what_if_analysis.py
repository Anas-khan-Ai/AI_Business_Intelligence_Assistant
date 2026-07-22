import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def show_what_if_analysis(
    df,
    sales_column,
    profit_column
):

    st.markdown("---")
    st.subheader("🎯 What-If Analysis")

    if df is None:
        st.warning("Please upload dataset first.")
        return

    data = df[[sales_column, profit_column]].dropna()

    X = data[[sales_column]]
    y = data[profit_column]

    model = LinearRegression()
    model.fit(X, y)

    st.markdown("### Change Sales Value")

    sales = st.slider(
        "Sales",
        float(data[sales_column].min()),
        float(data[sales_column].max()),
        float(data[sales_column].mean())
    )

    predicted_profit = model.predict([[sales]])[0]

    st.metric(
        "Predicted Profit",
        f"{predicted_profit:,.2f}"
    )

    profit_margin = (predicted_profit / sales) * 100

    st.metric(
        "Estimated Profit Margin",
        f"{profit_margin:.2f}%"
    )

    if predicted_profit > 0:
        st.success("Business remains profitable.")
    else:
        st.error("Business may go into loss.")

    st.markdown("### AI Suggestion")

    if profit_margin > 20:
        st.success("Excellent business scenario.")

    elif profit_margin > 10:
        st.info("Good business scenario.")

    elif profit_margin > 5:
        st.warning("Average profitability. Improve pricing.")

    else:
        st.error("Very low profitability. Reduce costs.")