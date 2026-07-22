import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)


def show_prediction(df, sales_column):

    st.markdown("---")
    st.subheader("📈 Sales Prediction")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    numeric_df = df.select_dtypes(include="number")

    if sales_column not in numeric_df.columns:
        st.error("Sales column must be numeric.")
        return

    if len(numeric_df.columns) < 2:
        st.error("Dataset needs at least 2 numeric columns.")
        return

    feature_column = st.selectbox(
        "Select Feature for Prediction",
        [col for col in numeric_df.columns if col != sales_column]
    )

    X = numeric_df[[feature_column]]
    y = numeric_df[sales_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    value = st.number_input(
        f"Enter {feature_column}",
        value=float(X[feature_column].mean())
    )

    if st.button("Predict Sales", key="predict_sales"):

        prediction = model.predict([[value]])[0]

        st.success(f"💰 Predicted Sales: {prediction:,.2f}")

        st.markdown("### 📊 Model Performance")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("R² Score", f"{r2:.3f}")

        with c2:
            st.metric("MAE", f"{mae:.2f}")

        with c3:
            st.metric("RMSE", f"{rmse:.2f}")

        result_df = pd.DataFrame({
            "Actual Sales": y_test.values,
            "Predicted Sales": y_pred
        })

        fig = px.scatter(
            result_df,
            x="Actual Sales",
            y="Predicted Sales",
            title="Actual vs Predicted Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "📥 Download Prediction CSV",
            result_df.to_csv(index=False),
            file_name="prediction_results.csv",
            mime="text/csv"
        )