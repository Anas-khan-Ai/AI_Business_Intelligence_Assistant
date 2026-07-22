import streamlit as st
import plotly.express as px
import pandas as pd

def show_charts(
    filtered_df,
    sales_column,
    profit_column,
    category_column,
    region_column,
    product_column
):
    
    # BUSINESS CHARTS
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("📊 Business Charts")

        chart_type = st.selectbox(
            "Select Chart",
            [
                "Sales by Category",
                "Sales by Region",
                "Profit by Category",
                "Top 10 Products",
                "Sales vs Profit",
                "Sales Distribution",
                "Correlation Heatmap"
            ]
        )

        if chart_type == "Sales by Category":

            chart = (
                filtered_df.groupby(category_column)[sales_column]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                chart,
                x=category_column,
                y=sales_column,
                title="Sales by Category"
            )

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Sales by Region":

            chart = (
                filtered_df.groupby(region_column)[sales_column]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                chart,
                x=region_column,
                y=sales_column,
                title="Sales by Region"
            )

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Profit by Category":

            chart = (
                filtered_df.groupby(category_column)[profit_column]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                chart,
                names=category_column,
                values=profit_column,
                title="Profit by Category"
            )

            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Top 10 Products":

            chart = (
                filtered_df.groupby(product_column)[sales_column]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            fig = px.bar(
                chart,
                x=product_column,
                y=sales_column,
                title="Top 10 Products by Sales",
                text_auto=True
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Top 10 Products")

            st.dataframe(chart, use_container_width=True)

        elif chart_type == "Sales vs Profit":

            fig = px.scatter(
                filtered_df,
                x=sales_column,
                y=profit_column,
                color=category_column,
                hover_data=[product_column],
                title="Sales vs Profit Analysis"
            )

            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Sales Distribution":

            fig = px.histogram(
                filtered_df,
                x=sales_column,
                nbins=30,
                title="Sales Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Correlation Heatmap":

            numeric_df = filtered_df.select_dtypes(include="number")

            corr = numeric_df.corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                title="Correlation Heatmap",
                aspect="auto"
            )

            st.plotly_chart(fig, use_container_width=True)
    