import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import plotly.express as px


def show_automl(df, sales_column):

    st.markdown("---")
    st.subheader("🤖 AutoML Prediction")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    if len(df) < 20:
        st.warning("⚠ Dataset should contain at least 20 rows for AutoML.")
        return

    numeric_df = df.select_dtypes(include=np.number)

    if sales_column not in numeric_df.columns:
        st.error("Sales column must be numeric.")
        return

    feature_columns = [
        col for col in numeric_df.columns
        if col != sales_column
    ]

    if len(feature_columns) == 0:
        st.error("No numeric features found.")
        return

    selected_features = st.multiselect(
        "Select Features",
        feature_columns,
        default=feature_columns
    )

    if len(selected_features) == 0:
        st.warning("Please select at least one feature.")
        return

    X = numeric_df[selected_features]
    y = numeric_df[sales_column]

    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    results = []

    best_model = None
    best_score = -999

    st.info("🚀 Training Models...")

    for name, model in models.items():

        try:

            model.fit(X_train, y_train)

            pred = model.predict(X_test)

            if len(y_test) < 2:
                r2 = 0
            else:
                r2 = r2_score(y_test, pred)

            mae = mean_absolute_error(y_test, pred)
            rmse = np.sqrt(mean_squared_error(y_test, pred))

            results.append({
                "Model": name,
                "R² Score": round(r2, 4),
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2)
            })

            if r2 > best_score:
                best_score = r2
                best_model = model

        except Exception as e:

            st.error(f"{name} failed")

            st.exception(e)

    if len(results) == 0:

        st.error("No model was trained successfully.")

        return

    results_df = pd.DataFrame(results)

    st.success("✅ Model Training Completed")

    st.markdown("## 📊 Model Comparison")

    st.dataframe(
        results_df,
        use_container_width=True
    )

    fig = px.bar(
        results_df,
        x="Model",
        y="R² Score",
        color="Model",
        text="R² Score",
        title="Model Performance Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        f"🏆 Best Model : {type(best_model).__name__}"
    )

    st.info(
        f"Best R² Score : {best_score:.4f}"
    )

    st.markdown("## 🎯 Predict Using Best Model")

    input_data = {}

    for feature in selected_features:

        input_data[feature] = st.number_input(
            f"Enter {feature}",
            value=float(X[feature].mean()),
            key=f"automl_{feature}"
        )

    if st.button("Predict"):

        input_df = pd.DataFrame([input_data])

        prediction = best_model.predict(input_df)[0]

        st.success(f"💰 Predicted {sales_column}: {prediction:,.2f}")

        result_df = pd.DataFrame({
            "Feature": list(input_data.keys()),
            "Value": list(input_data.values())
        })

        st.dataframe(
            result_df,
            use_container_width=True
        )

        csv = result_df.to_csv(index=False)

        st.download_button(
            "📥 Download Prediction",
            csv,
            file_name="prediction.csv",
            mime="text/csv"
        )

    if hasattr(best_model, "feature_importances_"):

        st.markdown("## 🌳 Feature Importance")

        importance = pd.DataFrame({

            "Feature": selected_features,

            "Importance": best_model.feature_importances_

        })

        importance = importance.sort_values(
            by="Importance",
            ascending=False
        )

        fig = px.bar(

            importance,

            x="Feature",

            y="Importance",

            color="Importance",

            text="Importance",

            title="Feature Importance"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            importance,
            use_container_width=True
        )