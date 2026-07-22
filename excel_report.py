import streamlit as st
import pandas as pd
from io import BytesIO


def show_excel_report(
    df,
    sales_column,
    profit_column,
    category_column,
    region_column,
    product_column
):

    st.markdown("---")
    st.subheader("📊 Excel Report Generator")

    if df is None:
        st.warning("Upload dataset first.")
        return

    # -----------------------
    # Summary
    # -----------------------

    summary = pd.DataFrame({

        "Metric": [
            "Total Sales",
            "Total Profit",
            "Total Orders",
            "Total Products",
            "Total Categories",
            "Total Regions"
        ],

        "Value": [

            df[sales_column].sum(),
            df[profit_column].sum(),
            len(df),
            df[product_column].nunique(),
            df[category_column].nunique(),
            df[region_column].nunique()

        ]

    })

    # -----------------------
    # Category Report
    # -----------------------

    category_report = (
        df.groupby(category_column)[
            [sales_column, profit_column]
        ]
        .sum()
        .reset_index()
    )

    # -----------------------
    # Region Report
    # -----------------------

    region_report = (
        df.groupby(region_column)[
            [sales_column, profit_column]
        ]
        .sum()
        .reset_index()
    )

    # -----------------------
    # Product Report
    # -----------------------

    product_report = (
        df.groupby(product_column)[
            [sales_column, profit_column]
        ]
        .sum()
        .reset_index()
    )

    # -----------------------
    # KPI Report
    # -----------------------

    kpi = pd.DataFrame({

        "KPI": [
            "Average Sales",
            "Average Profit",
            "Maximum Sales",
            "Maximum Profit",
            "Minimum Profit"
        ],

        "Value": [

            df[sales_column].mean(),
            df[profit_column].mean(),
            df[sales_column].max(),
            df[profit_column].max(),
            df[profit_column].min()

        ]

    })

    # -----------------------
    # Excel
    # -----------------------

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Raw Data",
            index=False
        )

        category_report.to_excel(
            writer,
            sheet_name="Category Report",
            index=False
        )

        region_report.to_excel(
            writer,
            sheet_name="Region Report",
            index=False
        )

        product_report.to_excel(
            writer,
            sheet_name="Product Report",
            index=False
        )

        kpi.to_excel(
            writer,
            sheet_name="KPI",
            index=False
        )

    st.success("Excel Report Ready ✅")

    st.download_button(

        "📥 Download Excel Report",

        data=output.getvalue(),

        file_name="AI_Business_Report.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )