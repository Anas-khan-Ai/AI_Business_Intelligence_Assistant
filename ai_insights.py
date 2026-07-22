import streamlit as st


def show_ai_insights(
    df,
    sales_column,
    profit_column,
    product_column,
    category_column,
    region_column
):

    st.markdown("---")
    st.subheader("🤖 AI Business Insights")

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()

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

    st.success("📈 AI Generated Business Insights")

    insights = []

    insights.append(
        f"💰 Total Sales : {total_sales:,.2f}"
    )

    insights.append(
        f"📈 Total Profit : {total_profit:,.2f}"
    )

    insights.append(
        f"🏆 Best Product : {best_product}"
    )

    insights.append(
        f"📉 Lowest Profit Product : {worst_product}"
    )

    insights.append(
        f"🌍 Best Performing Region : {best_region}"
    )

    insights.append(
        f"📦 Best Category : {best_category}"
    )

    insights.append(
        f"💹 Profit Margin : {profit_margin:.2f}%"
    )

    if profit_margin > 20:

        insights.append(
            "✅ Business performance is excellent."
        )

    elif profit_margin > 10:

        insights.append(
            "🟢 Business performance is good."
        )

    elif profit_margin > 5:

        insights.append(
            "🟡 Profit is average. Improve pricing strategy."
        )

    else:

        insights.append(
            "🔴 Profit is low. Reduce unnecessary costs."
        )

    st.markdown("### 📋 AI Report")

    for i in insights:

        st.info(i)

    st.markdown("### 💡 AI Recommendations")

    st.success(
        f"Increase marketing in **{best_region}**."
    )

    st.success(
        f"Keep sufficient stock of **{best_product}**."
    )

    st.warning(
        f"Review pricing of **{worst_product}**."
    )

    st.success(
        f"Focus more on **{best_category}** category."
    )