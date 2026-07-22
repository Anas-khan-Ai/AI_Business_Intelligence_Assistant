import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest


def show_anomaly_detection(
    df,
    sales_column,
    profit_column
):

    st.markdown("---")
    st.subheader("🚨 AI Anomaly Detection")

    if df is None:
        st.warning("Upload dataset first.")
        return

    data = df[[sales_column, profit_column]].copy()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    data["Anomaly"] = model.fit_predict(data)

    result = df.copy()

    result["Anomaly"] = data["Anomaly"]

    normal = result[result["Anomaly"] == 1]

    anomaly = result[result["Anomaly"] == -1]

    c1, c2 = st.columns(2)

    c1.metric(
        "Normal Transactions",
        len(normal)
    )

    c2.metric(
        "Anomalies",
        len(anomaly)
    )

    st.markdown("### 🚨 Suspicious Transactions")

    st.dataframe(
        anomaly,
        use_container_width=True
    )

    fig = px.scatter(
        result,
        x=sales_column,
        y=profit_column,
        color=result["Anomaly"].astype(str),
        title="Anomaly Detection"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Anomaly Report",
        anomaly.to_csv(index=False),
        file_name="anomaly_report.csv",
        mime="text/csv"
    )