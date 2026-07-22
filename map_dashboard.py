import streamlit as st
import pandas as pd
import plotly.express as px


def show_map_dashboard(
    df,
    region_column,
    sales_column,
    profit_column
):

    st.markdown("---")
    st.subheader("🗺️ Interactive Map Dashboard")

    region_data = (
        df.groupby(region_column)
        [[sales_column, profit_column]]
        .sum()
        .reset_index()
    )

    # Coordinates (India Example)
    coordinates = {
        "North": [28.6139, 77.2090],
        "South": [12.9716, 77.5946],
        "East": [22.5726, 88.3639],
        "West": [19.0760, 72.8777],
        "Central": [23.2599, 77.4126]
    }

    region_data["Latitude"] = region_data[region_column].map(
        lambda x: coordinates.get(x, [20.5937, 78.9629])[0]
    )

    region_data["Longitude"] = region_data[region_column].map(
        lambda x: coordinates.get(x, [20.5937, 78.9629])[1]
    )

    fig = px.scatter_mapbox(
        region_data,
        lat="Latitude",
        lon="Longitude",
        size=sales_column,
        color=profit_column,
        hover_name=region_column,
        hover_data=[sales_column, profit_column],
        zoom=3.8,
        height=600
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        region_data,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Region Report",
        region_data.to_csv(index=False),
        "region_map_report.csv",
        "text/csv"
    )