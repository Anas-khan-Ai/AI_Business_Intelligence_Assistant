import streamlit as st
import pandas as pd
import plotly.express as px
from charts import show_charts
from ai_chat import show_ai_chat
from dashboard import show_dashboard
from prediction import show_prediction
from preprocessing import show_preprocessing
from automl import show_automl
import traceback
from analysis import show_analysis
from kpi_dashboard import show_kpi_dashboard
from recommendation import show_recommendations
from pdf_report import show_pdf_download
from forecast import show_forecast
from market_basket import show_market_basket
from profit_leakage import show_profit_leakage
from executive_dashboard import show_executive_dashboard
from excel_report import show_excel_report
from map_dashboard import show_map_dashboard
from ai_insights import show_ai_insights
from anomaly_detection import show_anomaly_detection
from what_if_analysis import show_what_if_analysis
from data_cleaning_ai import show_data_cleaning_ai
import plotly.figure_factory as ff
import time

from google import genai



# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# GEMINI CLIENT
# -------------------------------------------------

client = genai.Client(
    api_key="AQ.Ab8RN6KmGA7QQNmIhb5fY5BFRwY_TdMe-gjSTElUfrYbUdGGWA"
)



# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    st.title("📊 AI BI Assistant")
    

    st.markdown("---")

    menu = st.radio(
        "📂 Select Module",
        [
            "🏠 Dashboard",
            "📊 Data Analysis",
        "📈 Interactive Charts",
        "💰 Business KPIs",
        "🤖 AutoML Prediction",
        "📉 Sales Forecasting",
        "🛒 Market Basket Analysis",
        "💡 Business Recommendations",
        "📉 Profit Leakage Analysis",
        "👔 AI Executive Dashboard",
        "📄 Smart PDF Report",
        "📊 Excel Report Generator",
        "🗺️ Interactive Map Dashboard",
        "🤖 AI Business Insights",
        "🚨 AI Anomaly Detection",
        "🎯 What-If Analysis",
        "🧹 AI Data Cleaning Assistant"
        ]
    )

    st.markdown("---")
    st.info("AI Powered Business Intelligence System")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("---")

st.info("🤖 AI Powered Business Intelligence System")

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown("""
# 🤖 AI Business Intelligence Assistant

### Enterprise Business Analytics Platform

Analyze • Predict • Forecast • Optimize

---
""")

st.success("""
### 🚀 System Status

✅ Dashboard Loaded Successfully

✅ AI Models Ready

✅ Analytics Engine Running

✅ Reports Available
""")

st.markdown("""

## 📋 Dashboard Overview

Welcome to the AI Business Intelligence Assistant.

This platform enables organizations to:

📊 Analyze Business Performance

📈 Visualize Sales & Profit Trends

🤖 Generate AI Powered Insights

📉 Forecast Future Sales

📄 Generate Professional Reports

🚀 Make Data Driven Business Decisions
""")
st.divider()

# -------------------------------------------------
# DASHBOARD METRICS (Dummy Data)

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

df = None

# -------------------------------------------------
# READ FILE
# -------------------------------------------------
if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):

            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")

            except UnicodeDecodeError:

                uploaded_file.seek(0)

                try:
                    df = pd.read_csv(uploaded_file, encoding="latin1")

                except UnicodeDecodeError:

                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding="cp1252")

        elif uploaded_file.name.endswith(".xlsx"):

            df = pd.read_excel(uploaded_file)

        st.success(f"✅ File Uploaded Successfully : {uploaded_file.name}")
        df = show_preprocessing(df)

        # -------------------------------------------------
        # DATASET PREVIEW
        # -------------------------------------------------

        st.subheader("📄 Dataset Preview")

        st.dataframe(df.head())

        # -------------------------------------------------
        # ROWS & COLUMNS
        # -------------------------------------------------

        rows, cols = df.shape

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Rows", rows)

        with c2:
            st.metric("Columns", cols)

        # -------------------------------------------------
        # MISSING VALUES
        # -------------------------------------------------

        st.subheader("📌 Missing Values")

        st.dataframe(df.isnull().sum())

        # -------------------------------------------------
        # DUPLICATE ROWS
        # -------------------------------------------------

        st.metric("Duplicate Rows", df.duplicated().sum())

        # -------------------------------------------------
        # DATA TYPES
        # -------------------------------------------------

        st.subheader("📌 Data Types")

        dtype_df = pd.DataFrame(df.dtypes, columns=["Data Type"])

        st.dataframe(dtype_df)

        # -------------------------------------------------
        # STATISTICAL SUMMARY
        # -------------------------------------------------

        st.subheader("📌 Statistical Summary")

        st.dataframe(df.describe(include="all"))

        # -------------------------------------------------
        # COLUMN NAMES
        # -------------------------------------------------

        st.subheader("📌 Columns")

        st.write(df.columns.tolist())


        # -------------------------------------------------
        # Dynamic Column Mapping
        # -------------------------------------------------

        st.subheader("🛠 Dynamic Column Mapping")

        columns = df.columns.tolist()

        sales_column = st.selectbox(
            "Select Sales Column",
            columns,
            index=columns.index("Sales") if "Sales" in columns else 0
        )

        profit_column = st.selectbox(
            "Select Profit Column",
            columns,
            index=columns.index("Profit") if "Profit" in columns else 0
        )

        product_column = st.selectbox(
            "Select Product Column",
            columns,
            index=columns.index("Product") if "Product" in columns else 0
        )

        category_column = st.selectbox(
            "Select Category Column",
            columns,
            index=columns.index("Category") if "Category" in columns else 0
        )

        region_column = st.selectbox(
            "Select Region Column",
            columns,
            index=columns.index("Region") if "Region" in columns else 0
        )
          
        total_sales, total_profit, total_orders, average_sales, summary = show_dashboard(
    df,
    sales_column,
    profit_column,
    product_column
)
        
                    # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("🎯 Dashboard Filters")

        f1, f2 = st.columns(2)

        with f1:
            selected_region = st.selectbox(
                "Select Region",
                ["All"] + sorted(df[region_column].astype(str).unique().tolist())
            )

        with f2:
            selected_category = st.selectbox(
                "Select Category",
                ["All"] + sorted(df[category_column].astype(str).unique().tolist())
            )

     
        filtered_df = df.copy()
        
        st.write(filtered_df.columns.tolist())

        if selected_region != "All":
           filtered_df = filtered_df[
                filtered_df[region_column] == selected_region
    ]
           

        if selected_category != "All":
         filtered_df = filtered_df[
             filtered_df[category_column] == selected_category
    ]
         
         
         quantity_column = "Quantity"
         show_kpi_dashboard(
               filtered_df,
               sales_column,
               profit_column,
              quantity_column
)

         show_charts(
              filtered_df,
              sales_column,
              profit_column,
              category_column,
              region_column,
              product_column
)

         show_prediction(
              filtered_df,
              sales_column
)

        show_automl(
             filtered_df,
             sales_column
)
        show_analysis(
            filtered_df,
            sales_column,
            profit_column,
            product_column,
            category_column,
            region_column
)
    
       
        show_recommendations(
             filtered_df,
             sales_column,
             profit_column,
             category_column,
             region_column,
             None
)
        quantity_column = "Quantity"
        show_pdf_download(
             filtered_df,
             sales_column,
             profit_column,
             quantity_column,
             region_column,
             category_column
)
        
        st.write("Columns:", filtered_df.columns.tolist())


        show_forecast(
             filtered_df,
             sales_column
) 
        customer_column = "Customer Name"
        st.write("Columns in Dataset")
        st.write(filtered_df.columns.tolist())

        show_market_basket(
             filtered_df
)
        show_profit_leakage(
            filtered_df,
            sales_column,
            profit_column,
            product_column,
            category_column,
            region_column
)
        show_executive_dashboard(
             filtered_df,
             sales_column,
             profit_column,
             product_column,
             category_column,
             region_column
)
        show_excel_report(
             filtered_df,
             sales_column,
             profit_column,
             category_column,
             region_column,
             product_column
)
        show_map_dashboard(
            filtered_df,
            region_column,
            sales_column,
            profit_column
)

        show_ai_insights(
             filtered_df,
             sales_column,
             profit_column,
             product_column,
             category_column,
             region_column
)
        show_anomaly_detection(
             filtered_df,
             sales_column,
             profit_column
)
        
        show_what_if_analysis(
            filtered_df,
            sales_column,
            profit_column
)
        

        

        show_ai_chat(
             client,
             filtered_df
)
        
        
        show_data_cleaning_ai(filtered_df)
            # Prediction bhi filters ke baad show karo
    
            
                   
        

                    # -------------------------------------------------
        # AI AUTO CHART GENERATOR
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("🤖 AI Auto Chart Generator")

        chart_query = st.text_input(
            "Ask AI to generate a chart",
            placeholder="Example: Show Sales by Region"
        )

        if st.button("Generate Chart"):

            query = chart_query.lower()

            if "sales" in query and "region" in query:

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

            elif "sales" in query and "category" in query:

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

            elif "profit" in query and "category" in query:

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

            elif "top" in query and "product" in query:

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
                    title="Top 10 Products"
                )

                st.plotly_chart(fig, use_container_width=True)

            else:

                st.warning("Chart not supported yet. Please try another query.")


        # -------------------------------------------------
        # SALES BY CATEGORY
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("📊 Sales by Category")

        category_sales = (
            filtered_df.groupby(category_column)[sales_column]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x=category_column,
            y=sales_column,
            color=category_column,
            title="Sales by Category"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # REGION WISE SALES
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("🥧 Region Wise Sales")

        region_sales = (
            filtered_df.groupby(region_column)[sales_column]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            region_sales,
            names=region_column,
            values=sales_column,
            title="Region Wise Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # TOP 10 PRODUCTS
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("🏆 Top 10 Products")

        top_products = (
            filtered_df.groupby(product_column)[sales_column]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x=sales_column,
            y=product_column,
            orientation="h",
            title="Top 10 Products"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # DATASET INFORMATION
        # -------------------------------------------------

        st.subheader("📌 Dataset Information")

        info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.values,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(info_df)

    except Exception:
     st.code(traceback.format_exc())
st.markdown("---")

# -------------------------------------------------
# MODULE DISPLAY
# -------------------------------------------------

st.subheader("Selected Module")

if menu == "🏠 Dashboard":
    st.success("Dashboard Loaded Successfully")

elif menu == "📁 Chat with CSV":
    st.info("🚧 CSV Chat Module will be added in next chapter.")

elif menu == "📄 Chat with PDF":
    st.info("🚧 PDF Chat Module will be added in next chapter.")

elif menu == "🗄 SQL Generator":
    st.info("🚧 SQL Generator Module will be added in next chapter.")

elif menu == "📈 Automatic Charts":
    st.info("🚧 Automatic Charts Module will be added in next chapter.")

elif menu == "📊 Sales Prediction":
    st.info("🚧 Sales Prediction Module will be added in next chapter.")

elif menu == "👥 Customer Segmentation":
    st.info("🚧 Customer Segmentation Module will be added in next chapter.")

elif menu == "📝 Report Generation":
    st.info("🚧 Report Generation Module will be added in next chapter.")

elif menu == "🎤 Voice Assistant":
    st.info("🚧 Voice Assistant Module will be added in next chapter.")

elif menu == "⚙ Settings":
    st.info("🚧 Settings Module will be added in next chapter.")

st.markdown("---")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
# -------------------------------------------------
