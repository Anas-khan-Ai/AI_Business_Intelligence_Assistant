import streamlit as st

def show_kpi_dashboard(
    df,
    sales_column,
    profit_column,
    quantity_column
):

    st.markdown("---")
    st.subheader("📊 Business KPI Dashboard")

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()
    total_orders = len(df)
    total_quantity = df[quantity_column].sum()

    avg_order_value = total_sales / total_orders

    profit_margin = 0

    if total_sales != 0:
        profit_margin = (total_profit / total_sales) * 100

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💰 Total Sales",
            f"{total_sales:,.2f}"
        )

        st.metric(
            "📦 Total Orders",
            total_orders
        )

    with c2:
        st.metric(
            "💵 Total Profit",
            f"{total_profit:,.2f}"
        )

        st.metric(
            "🛒 Quantity Sold",
            int(total_quantity)
        )

    with c3:
        st.metric(
            "📈 Avg Order Value",
            f"{avg_order_value:,.2f}"
        )

        st.metric(
            "📊 Profit Margin",
            f"{profit_margin:.2f}%"
        )

    st.markdown("---")

    score = 100

    if profit_margin < 10:
        score -= 30

    if total_profit < 0:
        score -= 40

    if score >= 90:
        status = "🟢 Excellent"

    elif score >= 70:
        status = "🟡 Good"

    else:
        status = "🔴 Needs Improvement"

    st.subheader("🤖 Business Health Score")

    st.progress(score / 100)

    st.success(f"Health Score : {score}/100")

    st.info(status)