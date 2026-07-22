import streamlit as st
import pandas as pd

from mlxtend.frequent_patterns import apriori, association_rules


def show_market_basket(df):

    st.markdown("---")
    st.subheader("🛒 Market Basket Analysis")

    # Check required columns
    if "Order ID" not in df.columns:
        st.error("Order ID column not found.")
        return

    if "Product" not in df.columns:
        st.error("Product column not found.")
        return

    # Create basket
    basket = (
        df.groupby(["Order ID", "Product"])
        .size()
        .unstack(fill_value=0)
    )

    basket = basket.astype(bool)

    st.write("### Basket Shape")
    st.write(basket.shape)

    st.write("### Products per Order")
    order_count = df.groupby("Order ID")["Product"].count()
    st.dataframe(order_count.head(20))

    st.write("Average Products per Order")
    st.write(order_count.mean())

    # Frequent Itemsets
    frequent_items = apriori(
        basket,
        min_support=0.01,
        use_colnames=True
    )

    st.write("Frequent Itemsets")
    st.dataframe(frequent_items)

    if frequent_items.empty:
        st.warning("No Frequent Itemsets Found.")
        return

    # Association Rules
    try:

        rules = association_rules(
            frequent_items,
            metric="confidence",
            min_threshold=0.01
        )

    except Exception as e:

        st.error(e)
        return

    if rules.empty:
        st.warning("No Association Rules Found.")

        st.info(
            """
Possible Reasons

• Every Order ID contains only one product

• Products are not repeating together

• Dataset is too small
            """
        )

        return

    rules = rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift"
        ]
    ]

    rules["antecedents"] = rules["antecedents"].apply(
        lambda x: ", ".join(list(x))
    )

    rules["consequents"] = rules["consequents"].apply(
        lambda x: ", ".join(list(x))
    )

    rules = rules.sort_values(
        by="lift",
        ascending=False
    )

    st.success("Market Basket Analysis Completed")

    st.dataframe(
        rules,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Rules",
        rules.to_csv(index=False),
        file_name="market_basket_rules.csv",
        mime="text/csv"
    )