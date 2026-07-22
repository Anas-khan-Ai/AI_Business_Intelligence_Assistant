import streamlit as st

def show_dashboard(
    df,
    sales_column,
    profit_column,
    product_column
):

    st.subheader("📊 Business KPI Dashboard")

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()
    total_orders = len(df)
    total_products = df[product_column].nunique()
    average_sales = df[sales_column].mean()

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric("💰 Total Sales", f"{total_sales:,.2f}")

    with k2:
        st.metric("📈 Total Profit", f"{total_profit:,.2f}")

    with k3:
        st.metric("📦 Orders", total_orders)

    with k4:
        st.metric("🛍 Products", total_products)

    with k5:
        st.metric("📊 Avg Sales", f"{average_sales:,.2f}")

    st.markdown("---")
    st.subheader("📋 Business Summary")

    highest_sales = df[sales_column].max()
    lowest_sales = df[sales_column].min()

    highest_profit = df[profit_column].max()
    lowest_profit = df[profit_column].min()

    summary = f"""
Total Orders : {total_orders}

Total Sales : {total_sales:,.2f}

Average Sales : {average_sales:,.2f}

Highest Sale : {highest_sales:,.2f}

Lowest Sale : {lowest_sales:,.2f}

Total Profit : {total_profit:,.2f}

Highest Profit : {highest_profit:,.2f}

Lowest Profit : {lowest_profit:,.2f}
"""

    st.text(summary)

    return (
        total_sales,
        total_profit,
        total_orders,
        average_sales,
        summary
    )