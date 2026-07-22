import streamlit as st
import plotly.express as px


def show_analysis(
    df,
    sales_column,
    profit_column,
    product_column,
    category_column,
    region_column
):

    st.markdown("---")
    st.subheader("📊 Advanced Business Analysis")

    tab1, tab2, tab3 = st.tabs([
        "🏆 Top Products",
        "📉 Bottom Products",
        "🌍 Region Analysis"
    ])

    # -----------------------------
    # TOP PRODUCTS
    # -----------------------------
    with tab1:

        top_products = (
            df.groupby(product_column)[sales_column]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        st.write("### 🏆 Top 10 Products")

        fig = px.bar(
            top_products,
            x=product_column,
            y=sales_column,
            color=sales_column,
            title="Top 10 Products by Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(top_products, use_container_width=True)

    # -----------------------------
    # BOTTOM PRODUCTS
    # -----------------------------
    with tab2:

        bottom_products = (
            df.groupby(product_column)[sales_column]
            .sum()
            .sort_values(ascending=True)
            .head(10)
            .reset_index()
        )

        st.write("### 📉 Bottom 10 Products")

        fig = px.bar(
            bottom_products,
            x=product_column,
            y=sales_column,
            color=sales_column,
            title="Bottom 10 Products by Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(bottom_products, use_container_width=True)

    # -----------------------------
    # REGION ANALYSIS
    # -----------------------------
    with tab3:

        region_sales = (
            df.groupby(region_column)[sales_column]
            .sum()
            .reset_index()
        )

        region_profit = (
            df.groupby(region_column)[profit_column]
            .sum()
            .reset_index()
        )

        st.write("### 🌍 Sales by Region")

        fig = px.pie(
            region_sales,
            names=region_column,
            values=sales_column,
            title="Sales Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("### 💰 Profit by Region")

        fig = px.bar(
            region_profit,
            x=region_column,
            y=profit_column,
            color=profit_column,
            title="Profit by Region"
        )

        st.plotly_chart(fig, use_container_width=True)