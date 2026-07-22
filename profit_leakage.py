import streamlit as st
import pandas as pd
import plotly.express as px


def show_profit_leakage(
    df,
    sales_column,
    profit_column,
    product_column,
    category_column,
    region_column
):

    st.markdown("---")
    st.subheader("📉 Profit Leakage Analysis")

    if df is None:
        st.warning("Upload dataset first.")
        return

    # -------------------------
    # Profit Margin
    # -------------------------

    data = df.copy()

    data["Profit Margin (%)"] = (
        data[profit_column] /
        data[sales_column]
    ) * 100

    # -------------------------
    # Loss Products
    # -------------------------

    st.markdown("### 🔴 Loss Making Products")

    loss_products = (
        data.groupby(product_column)[profit_column]
        .sum()
        .reset_index()
        .sort_values(
            by=profit_column
        )
    )

    loss_products = loss_products[
        loss_products[profit_column] < 0
    ]

    if loss_products.empty:
        st.success("No Loss Making Products 🎉")
    else:

        st.dataframe(
            loss_products,
            use_container_width=True
        )

        fig = px.bar(
            loss_products,
            x=product_column,
            y=profit_column,
            color=profit_column,
            title="Loss Making Products"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------
    # Category Leakage
    # -------------------------

    st.markdown("### 📦 Profit by Category")

    category_profit = (
        data.groupby(category_column)[profit_column]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_profit,
        x=category_column,
        y=profit_column,
        color=profit_column,
        title="Category Profit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # Region Leakage
    # -------------------------

    st.markdown("### 🌍 Profit by Region")

    region_profit = (
        data.groupby(region_column)[profit_column]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_profit,
        names=region_column,
        values=profit_column,
        title="Region Profit Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # Worst Transactions
    # -------------------------

    st.markdown("### ⚠ Worst Transactions")

    worst = data.sort_values(
        by=profit_column
    ).head(10)

    st.dataframe(
        worst,
        use_container_width=True
    )

    # -------------------------
    # Profit Margin
    # -------------------------

    st.markdown("### 💰 Profit Margin")

    fig = px.histogram(
        data,
        x="Profit Margin (%)",
        nbins=30,
        title="Profit Margin Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # Download
    # -------------------------

    csv = data.to_csv(index=False)

    st.download_button(
        "📥 Download Profit Leakage Report",
        csv,
        "profit_leakage.csv",
        "text/csv"
    )