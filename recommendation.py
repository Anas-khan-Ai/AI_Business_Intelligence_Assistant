import streamlit as st


def show_recommendations(
    df,
    sales_column,
    profit_column,
    category_column,
    region_column,
    discount_column=None
):

    st.markdown("---")
    st.subheader("🤖 AI Business Recommendations")

    total_sales = df[sales_column].sum()
    total_profit = df[profit_column].sum()

    profit_margin = 0

    if total_sales != 0:
        profit_margin = (total_profit / total_sales) * 100

    best_region = (
        df.groupby(region_column)[sales_column]
        .sum()
        .idxmax()
    )

    worst_region = (
        df.groupby(region_column)[sales_column]
        .sum()
        .idxmin()
    )

    best_category = (
        df.groupby(category_column)[sales_column]
        .sum()
        .idxmax()
    )

    worst_category = (
        df.groupby(category_column)[sales_column]
        .sum()
        .idxmin()
    )

    st.success(f"🏆 Best Region : {best_region}")
    st.error(f"📉 Lowest Region : {worst_region}")

    st.success(f"🏆 Best Category : {best_category}")
    st.error(f"📉 Lowest Category : {worst_category}")

    st.markdown("## 💡 AI Suggestions")

    if profit_margin < 10:
        st.warning(
            "⚠️ Profit Margin is below 10%. Try reducing unnecessary discounts."
        )
    else:
        st.success(
            "✅ Profit Margin looks healthy."
        )

    if total_profit < 0:
        st.error(
            "❌ Overall business is running in loss."
        )

    st.info(
        f"📈 Focus more marketing on **{best_region}** region."
    )

    st.info(
        f"🛍 Increase inventory for **{best_category}** category."
    )

    st.warning(
        f"📉 Improve performance of **{worst_category}** category."
    )

    st.warning(
        f"🌍 Create new offers for **{worst_region}** region."
    )

    if (
    discount_column is not None
    and discount_column in df.columns
):

        avg_discount = df[discount_column].mean()

        if avg_discount > 0.30:
            st.warning(
                "⚠️ Average discount is high. Consider reducing discounts."
            )

    score = 100

    if profit_margin < 10:
        score -= 20

    if total_profit < 0:
        score -= 40

    if score >= 90:
        health = "🟢 Excellent"

    elif score >= 70:
        health = "🟡 Good"

    else:
        health = "🔴 Needs Improvement"

    st.markdown("---")

    st.subheader("📊 Business Health")

    st.progress(score / 100)

    st.metric("Health Score", f"{score}/100")

    st.info(health)