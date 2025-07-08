import streamlit as st
import pandas as pd
import altair as alt

# ✅ Custom CSS for white select boxes
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom right, #5D4037, #8D6E63);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    .stSelectbox div div {
        background-color: #ffffff !important;
        color: #4E342E !important;
    }
    .stSelectbox div div div {
        background-color: #ffffff !important;
        color: #4E342E !important;
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Drill-down Pivot")

if 'fact_table' not in st.session_state:
    st.warning("Run ETL first.")
    st.stop()

df = st.session_state['fact_table']

# ✅ Show all columns
st.write("**Available columns:**", list(df.columns))

# ✅ Safe selectboxes
x = st.selectbox("X-axis (group by)", df.columns.tolist())
y = st.selectbox("Y-axis (value to sum)", df.columns.tolist())

st.write("🔍 **X selected:**", x)
st.write("🔍 **Y selected:**", y)

# ✅ Safe slicing with explicit checks
if x in df.columns and y in df.columns:
    try:
        sample = df[[x, y]].head()
        st.write("**Sample data:**", sample)
    except Exception as e:
        st.error(f"🚫 Could not show sample: {e}")

    # ✅ Safe pivot
    try:
        pivot = pd.pivot_table(df, index=x, values=y, aggfunc='sum')
        st.dataframe(pivot)

        chart = alt.Chart(pivot.reset_index()).mark_bar().encode(
            x=x,
            y=y
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Could not create pivot/chart: {e}")

else:
    st.error(f"Column not found: X=`{x}` Y=`{y}`")
