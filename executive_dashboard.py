import streamlit as st
import pandas as pd


def show_executive_dashboard(
    df,
    sales_column,
    profit_column,
    product_column,
    category_column,
    region_column
):

    st.markdown("---")
    st.subheader("👔 AI Executive Dashboard")

    if df is None:
        st.warning("Please upload dataset first.")
        return

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()
    total_orders = len(df)

    best_product = (
        df.groupby(product_column)[sales_column]
        .sum()
        .idxmax()
    )

    worst_product = (
        df.groupby(product_column)[profit_column]
        .sum()
        .idxmin()
    )

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

    profit_margin = (total_profit / total_sales) * 100

    if profit_margin >= 20:
        health = 95
        status = "🟢 Excellent"

    elif profit_margin >= 10:
        health = 80
        status = "🟢 Good"

    elif profit_margin >= 5:
        health = 65
        status = "🟡 Average"

    else:
        health = 40
        status = "🔴 Poor"

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Total Sales",
        f"{total_sales:,.2f}"
    )

    c2.metric(
        "📈 Total Profit",
        f"{total_profit:,.2f}"
    )

    c3.metric(
        "📦 Total Orders",
        total_orders
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.success(f"🏆 Best Product : {best_product}")

        st.success(f"🌍 Best Region : {best_region}")

        st.success(f"📦 Best Category : {best_category}")

    with c2:

        st.error(f"📉 Worst Product : {worst_product}")

        st.info(f"💹 Profit Margin : {profit_margin:.2f}%")

        st.info(f"🏥 Business Health : {health}/100")

    st.markdown("## 🤖 AI Business Summary")

    st.success(f"""
Business Status : {status}

✔ Total Sales : {total_sales:,.2f}

✔ Total Profit : {total_profit:,.2f}

✔ Best Product : {best_product}

✔ Best Region : {best_region}

✔ Best Category : {best_category}

✔ Profit Margin : {profit_margin:.2f}%
""")

    st.markdown("## 💡 AI Recommendations")

    if profit_margin < 10:

        st.warning("Reduce discount on low profit products.")

        st.warning("Increase marketing for profitable products.")

    else:

        st.success("Business is performing well.")

        st.success("Increase inventory of best-selling products.")

    st.success(f"Focus on **{best_region}** region.")

    st.success(f"Promote **{best_category}** category.")