from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import streamlit as st
import os


def generate_pdf(
    df,
    sales_column,
    profit_column,
    quantity_column,
    region_column,
    category_column
):

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()
    total_orders = len(df)
    if quantity_column in df.columns:
     total_quantity = df[quantity_column].sum()
    else:
     total_quantity = "N/A"

    best_region = (
        df.groupby(region_column)[sales_column]
        .sum()
        .idxmax()
    )

    best_category = (
        df.groupby(category_column)[sales_column]
        .sum()
        .idxmax()
    )

    file_name = "Business_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>AI Business Intelligence Report</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        )
    )

    data = [
        ["Metric", "Value"],
        ["Total Sales", f"{total_sales:,.2f}"],
        ["Total Profit", f"{total_profit:,.2f}"],
        ["Total Orders", total_orders],
        ["Best Region", best_region],
        ["Best Category", best_category]
]

    if total_quantity != "N/A":
     data.insert(4, ["Quantity Sold", total_quantity])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.blue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    elements.append(table)

    elements.append(
        Paragraph(
            "<br/><b>AI Recommendation</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"""
            Focus marketing on <b>{best_region}</b> region.

            Increase inventory for
            <b>{best_category}</b> category.

            Overall business performance looks healthy.
            """,
            styles["BodyText"]
        )
    )

    doc.build(elements)

    return file_name


def show_pdf_download(
    df,
    sales_column,
    profit_column,
    quantity_column,
    region_column,
    category_column
):

    st.markdown("---")

    st.subheader("📄 Smart PDF Report")

    if st.button("📥 Generate PDF Report"):

        pdf_file = generate_pdf(

            df,
            sales_column,
            profit_column,
            quantity_column,
            region_column,
            category_column

        )

        with open(pdf_file, "rb") as f:

            st.download_button(

                "⬇ Download PDF",

                f,

                file_name="Business_Report.pdf",

                mime="application/pdf"

            )

        os.remove(pdf_file)