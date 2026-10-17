
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
st.set_page_config(
    page_title="SmartGTM Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("SmartGTM - Go-To-Market Strategy Assistant")
st.write("Upload your marketing data to analyze business performance.")

# Sample data shown before a file is uploaded
sample_data = {
    "Channel": [
        "Social Media", "Email", "Search Ads",
        "Social Media", "Email", "Search Ads"
    ],
    "Leads": [120, 90, 150, 140, 110, 180],
    "Conversions": [18, 20, 30, 25, 24, 36],
    "Marketing Spend": [6000, 3000, 8000, 6500, 3500, 9000]
}

# CSV and Excel upload
st.sidebar.header("Upload Your Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(
                uploaded_file,
                engine="openpyxl"
            )

        st.sidebar.success("File uploaded successfully!")

    except Exception as e:
        st.error(f"Unable to read the file: {e}")
        st.stop()
else:
    df = pd.DataFrame(sample_data)
    st.info(
        "Showing sample data. Upload a file using the sidebar."
    )

# Check the required column names
required_columns = [
    "Channel",
    "Leads",
    "Conversions",
    "Marketing Spend"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.write("Your file must contain these columns:")
    st.write(required_columns)
    st.stop()

# Keep only the columns used by this dashboard

has_date = "Date" in df.columns

columns_to_keep = required_columns.copy()

if has_date:
    columns_to_keep.append("Date")

df = df[columns_to_keep].copy()

if has_date:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# Clean and validate values
df["Channel"] = df["Channel"].astype("string").str.strip()

for col in ["Leads", "Conversions", "Marketing Spend"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=required_columns)
df = df[df["Channel"] != ""]

if df.empty:
    st.error("The file does not contain any valid data rows.")
    st.stop()

if (df[["Leads", "Conversions", "Marketing Spend"]] < 0).any().any():
    st.error("Leads, conversions, and spend cannot be negative.")
    st.stop()

if (df["Conversions"] > df["Leads"]).any():
    st.warning(
        "Some rows have more conversions than leads. "
        "Please check the uploaded data."
    )

# Filter data by marketing channel
st.sidebar.header("Filter Dashboard")

available_channels = sorted(
    df["Channel"].dropna().unique().tolist()
)

selected_channels = st.sidebar.multiselect(
    "Select marketing channels",
    options=available_channels,
    default=available_channels
)

df = df[df["Channel"].isin(selected_channels)].copy()

if df.empty:
    st.warning("Select at least one marketing channel to view results.")
    st.stop()

# Calculate overall metrics
total_leads = df["Leads"].sum()
total_conversions = df["Conversions"].sum()
total_spend = df["Marketing Spend"].sum()

conversion_rate = (
    total_conversions / total_leads * 100
    if total_leads > 0 else 0
)

cost_per_lead = (
    total_spend / total_leads
    if total_leads > 0 else 0
)

cost_per_conversion = (
    total_spend / total_conversions
    if total_conversions > 0 else 0
)

# Display key performance indicators
st.subheader("Business Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", f"{total_leads:,.0f}")
col2.metric("Conversions", f"{total_conversions:,.0f}")
col3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
col4.metric("Cost per Lead", f"₹{cost_per_lead:,.2f}")

st.metric(
    "Cost per Conversion",
    f"₹{cost_per_conversion:,.2f}"
)

# Display the data table
st.subheader("Marketing Campaign Data")
st.dataframe(df, use_container_width=True)

# Campaign Date Analysis
st.subheader("Campaign Trends Over Time")

if has_date:
    dated_df = df.dropna(subset=["Date"]).copy()

    if not dated_df.empty:
        daily_data = dated_df.groupby(
            "Date", as_index=False
        ).agg({
            "Leads": "sum",
            "Conversions": "sum",
            "Marketing Spend": "sum"
        }).sort_values("Date")

        trend_choice = st.selectbox(
            "Choose a metric to analyze",
            ["Leads", "Conversions", "Marketing Spend"]
        )

        fig_trend = px.line(
            daily_data,
            x="Date",
            y=trend_choice,
            markers=True,
            title=f"{trend_choice} Over Time"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

        st.dataframe(
            daily_data,
            use_container_width=True
        )
    else:
        st.warning(
            "The Date column exists, but no valid dates were found."
        )
else:
    st.info(
        "To view campaign trends, upload a CSV or Excel file "
        "with an additional Date column."
    )


# Download Reports
st.subheader("Download Reports")

# Prepare CSV file
csv_data = df.to_csv(index=False).encode("utf-8-sig")

# Prepare Excel file
excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:
    df.to_excel(
        writer,
        index=False,
        sheet_name="Marketing Data"
    )

# Display download buttons
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="smartgtm_report.csv",
        mime="text/csv"
    )

with col2:
    st.download_button(
        label="Download as Excel",
        data=excel_buffer.getvalue(),
        file_name="smartgtm_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Summarize results by channel
channel_data = df.groupby(
    "Channel", as_index=False
).agg({
    "Leads": "sum",
    "Conversions": "sum",
    "Marketing Spend": "sum"
})

channel_data["Conversion Rate (%)"] = (
    channel_data["Conversions"]
    / channel_data["Leads"].replace(0, float("nan"))
    * 100
)

channel_data["Cost per Lead"] = (
    channel_data["Marketing Spend"]
    / channel_data["Leads"].replace(0, float("nan"))
)

# Channel Performance Insights
channel_data["Cost per Conversion"] = (
    channel_data["Marketing Spend"]
    / channel_data["Conversions"].replace(0, float("nan"))
)

st.subheader("Channel Performance Insights")

# Display channel comparison table
performance_table = channel_data[
    [
        "Channel",
        "Leads",
        "Conversions",
        "Marketing Spend",
        "Conversion Rate (%)",
        "Cost per Lead",
        "Cost per Conversion"
    ]
].sort_values(
    "Conversion Rate (%)",
    ascending=False,
    na_position="last"
)

st.dataframe(
    performance_table.style.format({
        "Marketing Spend": "₹{:,.2f}",
        "Conversion Rate (%)": "{:.2f}%",
        "Cost per Lead": "₹{:,.2f}",
        "Cost per Conversion": "₹{:,.2f}"
    }, na_rep="N/A"),
    use_container_width=True
)

# Identify the strongest conversion rate
valid_rates = channel_data.dropna(
    subset=["Conversion Rate (%)"]
)

# Identify the lowest cost per conversion
valid_costs = channel_data.dropna(
    subset=["Cost per Conversion"]
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Highest Conversion Rate**")

    if not valid_rates.empty:
        best_rate = valid_rates.loc[
            valid_rates["Conversion Rate (%)"].idxmax()
        ]

        st.metric(
            label=str(best_rate["Channel"]),
            value=f'{best_rate["Conversion Rate (%)"]:.2f}%'
        )
    else:
        st.info("No channel has enough leads to calculate a rate.")

with col2:
    st.markdown("**Lowest Cost per Conversion**")

    if not valid_costs.empty:
        lowest_cost = valid_costs.loc[
            valid_costs["Cost per Conversion"].idxmin()
        ]

        st.metric(
            label=str(lowest_cost["Channel"]),
            value=f'₹{lowest_cost["Cost per Conversion"]:,.2f}'
        )
    else:
        st.info("No conversions are available to calculate this cost.")

# Chart 1: Leads by channel
st.subheader("Leads by Marketing Channel")

fig1 = px.bar(
    channel_data,
    x="Channel",
    y="Leads",
    color="Channel",
    title="Total Leads Generated by Channel"
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Conversions by channel
st.subheader("Conversions by Marketing Channel")

fig2 = px.bar(
    channel_data,
    x="Channel",
    y="Conversions",
    color="Channel",
    title="Total Conversions by Channel"
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Spend versus conversions
st.subheader("Marketing Spend vs Conversions")

fig3 = px.scatter(
    channel_data,
    x="Marketing Spend",
    y="Conversions",
    size="Leads",
    color="Channel",
    hover_data=["Conversion Rate (%)", "Cost per Lead"],
    title="Marketing Spend and Conversions by Channel"
)

st.plotly_chart(fig3, use_container_width=True)

# Basic marketing insight
best_channel = channel_data.loc[
    channel_data["Leads"].idxmax(), "Channel"
]

st.subheader("Initial Marketing Insight")
st.info(
    f"{best_channel} generated the most leads in this dataset. "
    "Compare conversion rates and costs before deciding "
    "which channel performs best overall."
)
