import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import LinearRegression


def show_forecast(df, sales_column):

    st.markdown("---")
    st.subheader("📈 Sales Forecast")

    if df is None:
        st.warning("Please upload dataset first.")
        return

    if sales_column not in df.columns:
        st.error("Sales column not found.")
        return

    sales = df[sales_column].reset_index(drop=True)

    x = np.arange(len(sales)).reshape(-1, 1)
    y = sales.values

    model = LinearRegression()
    model.fit(x, y)

    forecast_days = st.slider(
        "Forecast Points",
        10,
        100,
        30
    )

    future_x = np.arange(
        len(sales),
        len(sales) + forecast_days
    ).reshape(-1, 1)

    future_pred = model.predict(future_x)

    history = pd.DataFrame({
        "Index": np.arange(len(sales)),
        "Sales": sales,
        "Type": "Historical"
    })

    future = pd.DataFrame({
        "Index": np.arange(
            len(sales),
            len(sales) + forecast_days
        ),
        "Sales": future_pred,
        "Type": "Forecast"
    })

    result = pd.concat([history, future])

    fig = px.line(
        result,
        x="Index",
        y="Sales",
        color="Type",
        title="Sales Forecast"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(future, use_container_width=True)

    st.download_button(
        "📥 Download Forecast",
        future.to_csv(index=False),
        file_name="forecast.csv",
        mime="text/csv"
    )