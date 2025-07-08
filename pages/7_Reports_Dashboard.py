import streamlit as st
import pandas as pd
import altair as alt
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom right, #5D4037, #8D6E63);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    .stApp {
        background-color: #ffffff;
    }

    .stApp, .stApp * {
        color: #4E342E;
    }

    div[data-testid="metric-container"] {
        background: rgba(93, 64, 55, 0.05);
        border-radius: 8px;
        padding: 10px;
    }

    /* ✅ Make selectbox dropdown & items white */
    .stSelectbox div div {
        background-color: #ffffff !important;
        color: #4E342E !important;
    }

    .stSelectbox div div div {
        background-color: #ffffff !important;
        color: #4E342E !important;
    }

    /* ✅ Make multiselect items white */
    .stMultiSelect div {
        background-color: #ffffff !important;
        color: #4E342E !important;
    }

    .stMultiSelect div div {
        background-color: #ffffff !important;
        color: #4E342E !important;
    }

    /* ✅ Make radio buttons white */
    div[data-baseweb="radio"] label {
        background-color: #ffffff !important;
        color: #4E342E !important;
        padding: 4px 8px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("📈 Data Warehouse Reports & Dashboard")

if 'fact_table' not in st.session_state:
    st.warning("⚠️ Please run ETL first to load the DW.")
    st.stop()

df = st.session_state['fact_table'].copy()

# --- Filters ---
st.sidebar.header("🔍 Filter Your Data")

# Optional: Date filter
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range",
                                       [min_date, max_date],
                                       min_value=min_date,
                                       max_value=max_date)
    if len(date_range) == 2:
        df = df[(df['Date'] >= pd.to_datetime(date_range[0])) &
                (df['Date'] <= pd.to_datetime(date_range[1]))]

# Optional: Category filter
if 'Category' in df.columns:
    categories = df['Category'].unique().tolist()
    selected_cats = st.sidebar.multiselect("Category", categories, default=categories)
    df = df[df['Category'].isin(selected_cats)]

# Optional: Product filter
if 'Product' in df.columns:
    products = df['Product'].unique().tolist()
    selected_products = st.sidebar.multiselect("Product", products, default=products)
    df = df[df['Product'].isin(selected_products)]

# --- Metrics ---
st.subheader("✅ Key Metrics")

if 'Amount' in df.columns:
    st.metric("Total Amount", f"${df['Amount'].sum():,.2f}")
    st.metric("Average Order", f"${df['Amount'].mean():,.2f}")
    st.metric("Max Order", f"${df['Amount'].max():,.2f}")

# --- Category Breakdown ---
st.subheader("✅ Category Breakdown")

if 'Category' in df.columns and 'Amount' in df.columns:
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category:N", sort='-y'),
        y="sum(Amount):Q",
        color="Category:N",
        tooltip=['Category', 'sum(Amount)']
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

# --- Drill-down ---
st.subheader("✅ Drill-down Table")

if 'Product' in df.columns and 'Amount' in df.columns:
    group_by = st.selectbox("Group By:", options=['Product', 'Category', 'Date'])
    pivot = df.groupby(group_by)['Amount'].sum().reset_index().sort_values('Amount', ascending=False)
    pivot.columns = [group_by, 'Total_Amount']
    st.dataframe(pivot)

# --- Time Trend ---
st.subheader("✅ Time Trend")

if 'Date' in df.columns and 'Amount' in df.columns:
    trend_metric = st.radio("Metric:", options=['sum', 'mean'])
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Date:T"),
        y=alt.Y(f"{trend_metric}(Amount):Q"),
        tooltip=['Date', f"{trend_metric}(Amount)"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)
