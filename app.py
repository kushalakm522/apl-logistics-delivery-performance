import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="APL Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("APL_Logistics_Cleaned.csv", encoding="latin1")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.caption(
    "Use the filters below to explore delivery performance."
)

# Reset Filters Button

if st.sidebar.button("🔄 Reset Filters"):
    st.session_state["selected_modes"] = sorted(
        df["Shipping Mode"].dropna().unique()
    )
    st.session_state["selected_markets"] = sorted(
        df["Market"].dropna().unique()
    )
    st.session_state["selected_regions"] = sorted(
        df["Order Region"].dropna().unique()
    )
    st.session_state["selected_segments"] = sorted(
        df["Customer Segment"].dropna().unique()
    )
    st.rerun()

selected_modes = st.sidebar.multiselect(
    "Shipping Mode",
    options=sorted(df["Shipping Mode"].dropna().unique()),
    default=sorted(df["Shipping Mode"].dropna().unique()),
    key="selected_modes"
)

selected_markets = st.sidebar.multiselect(
    "Market",
    options=sorted(df["Market"].dropna().unique()),
    default=sorted(df["Market"].dropna().unique()),
    key="selected_markets"
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Order Region"].dropna().unique()),
    default=sorted(df["Order Region"].dropna().unique()),
    key="selected_regions"
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer Segment"].dropna().unique()),
    default=sorted(df["Customer Segment"].dropna().unique()),
    key="selected_segments"
)

filtered_df = df[
    df["Shipping Mode"].isin(selected_modes)
    & df["Market"].isin(selected_markets)
    & df["Order Region"].isin(selected_regions)
    & df["Customer Segment"].isin(selected_segments)
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚚 APL Logistics Delivery Performance Dashboard")

st.write(
    "Delivery Performance, Delay Risk, and Logistics Efficiency "
    "Analysis in Global Supply Chain Operations"
)

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_orders = len(filtered_df)

delay_rate = (
    (filtered_df["Delay Gap"] > 0).mean() * 100
)

on_time_early_rate = (
    (filtered_df["Delay Gap"] <= 0).mean() * 100
)

average_delay = filtered_df["Delay Gap"].mean()

late_delivery_risk = (
    filtered_df["Late_delivery_risk"].mean() * 100
)# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "On-Time / Early Rate",
    f"{on_time_early_rate:.2f}%"
)

col3.metric(
    "Delay Rate",
    f"{delay_rate:.2f}%"
)

col4.metric(
    "Average Delay",
    f"{average_delay:.2f} days"
)

col5.metric(
    "Late Delivery Risk",
    f"{late_delivery_risk:.2f}%"
)

# ---------------------------------------------------
# PROJECT OVERVIEW
# ---------------------------------------------------

st.header("📋 Project Overview")

st.write("""
This dashboard analyzes shipment delivery performance across
shipping modes, markets, regions, and customer segments.

The main objectives are to identify delivery delays, evaluate
late delivery risk, and compare logistics efficiency.
""")

st.info(
    "Note: The dataset does not contain a genuine order/delivery "
    "date field, so a date-range filter is not applied."
)

# ---------------------------------------------------
# SHIPPING MODE ANALYSIS
# ---------------------------------------------------

st.header("🚚 Shipping Mode Performance")

shipping_mode_analysis = filtered_df.groupby("Shipping Mode").agg(
    Orders=("Shipping Mode", "count"),
    Average_Delay=("Delay Gap", "mean"),
    Delay_Rate=("Delay Gap", lambda x: (x > 0).mean() * 100),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

shipping_mode_analysis["Late_Risk"] = (
    shipping_mode_analysis["Late_Risk"] * 100
)

st.subheader("Delayed Shipment Rate by Shipping Mode")

st.bar_chart(
    shipping_mode_analysis,
    x="Shipping Mode",
    y="Delay_Rate"
)

st.dataframe(
    shipping_mode_analysis,
    use_container_width=True
)

# ---------------------------------------------------
# MARKET ANALYSIS
# ---------------------------------------------------

st.header("🌍 Market Performance")

market_analysis = filtered_df.groupby("Market").agg(
    Orders=("Market", "count"),
    Average_Delay=("Delay Gap", "mean"),
    Delay_Rate=("Delay Gap", lambda x: (x > 0).mean() * 100),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

market_analysis["Late_Risk"] = (
    market_analysis["Late_Risk"] * 100
)

st.subheader("Delayed Shipment Rate by Market")

st.bar_chart(
    market_analysis,
    x="Market",
    y="Delay_Rate"
)

st.dataframe(
    market_analysis,
    use_container_width=True
)
# ---------------------------------------------------
# REGION ANALYSIS
# ---------------------------------------------------

st.header("🌎 Regional Performance")

region_analysis = filtered_df.groupby("Order Region").agg(
Orders=("Order Region", "count"),
    Average_Delay=("Delay Gap", "mean"),
    Delay_Rate=("Delay Gap", lambda x: (x > 0).mean() * 100),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

region_analysis["Late_Risk"] = (
    region_analysis["Late_Risk"] * 100
)

region_analysis = region_analysis.sort_values(
    "Delay_Rate",
    ascending=False
)

top_regions = region_analysis.head(10)

st.subheader("Top 10 Regions by Delayed Shipment Rate")

st.bar_chart(
    top_regions,
    x="Order Region",
    y="Delay_Rate",
    horizontal=True
)

st.subheader("Regional Analysis Table")

st.dataframe(
    top_regions,
    use_container_width=True
)

# ---------------------------------------------------
# CUSTOMER SEGMENT ANALYSIS
# ---------------------------------------------------

st.header("👥 Customer Segment Performance")

segment_analysis = filtered_df.groupby("Customer Segment").agg(
    Orders=("Customer Segment", "count"),
    Average_Delay=("Delay Gap", "mean"),
    Delay_Rate=("Delay Gap", lambda x: (x > 0).mean() * 100),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

segment_analysis["Late_Risk"] = (
    segment_analysis["Late_Risk"] * 100
)

st.subheader("Delayed Shipment Rate by Customer Segment")

st.bar_chart(
    segment_analysis,
    x="Customer Segment",
    y="Delay_Rate"
)

st.subheader("Customer Segment Analysis Table")

st.dataframe(
    segment_analysis,
    use_container_width=True
)

# ---------------------------------------------------
# DELIVERY STATUS ANALYSIS
# ---------------------------------------------------

st.header("📦 Delivery Status Analysis")

delivery_status = filtered_df["Delivery Status"].value_counts().reset_index()

delivery_status.columns = ["Delivery Status", "Orders"]

delivery_status["Percentage"] = (
    delivery_status["Orders"] / len(filtered_df) * 100
)
st.subheader("Shipment Count by Delivery Status")

st.bar_chart(
    delivery_status,
    x="Delivery Status",
    y="Orders"
)

st.subheader("Delivery Status Table")

st.dataframe(
    delivery_status,
    use_container_width=True
)
# ---------------------------------------------------
# DELAY GAP DISTRIBUTION
# ---------------------------------------------------

st.header("⏱️ Delay Gap Distribution")

delay_gap_analysis = (
    filtered_df["Delay Gap"]
    .value_counts()
    .sort_index()
    .reset_index()
)

delay_gap_analysis.columns = ["Delay Gap", "Orders"]

st.subheader("Number of Shipments by Delay Gap")

st.bar_chart(
    delay_gap_analysis,
    x="Delay Gap",
    y="Orders"
)

st.subheader("Delay Gap Analysis Table")

st.dataframe(
    delay_gap_analysis,
    use_container_width=True
)




