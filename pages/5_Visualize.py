import streamlit as st
import pandas as pd
import altair as alt
# Apply custom CSS
st.markdown(
    """
    <style>
    /* st.write containers: white */
.css-1cpxqw2, .css-1xarl3l, .stMarkdown {
  background-color: #ffffff !important;
  color: #4E342E !important;
  padding: 10px;
  border-radius: 5px;
}
    /* Sidebar: brown gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom right, #5D4037, #8D6E63);
    }

    /* Sidebar text: white */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* Selectbox input & dropdown options background white */
.stSelectbox div div {
  background-color: #ffffff !important;
  color: #4E342E !important;
}

.stSelectbox div div div {
  background-color: #ffffff !important;
  color: #4E342E !important;
}

    /* Main content area: white background */
    .stApp {
        background-color: #ffffff;
    }

    /* Main text: dark brown */
    .stApp, .stApp * {
        color: #4E342E;
    }

    /* Optional: metric containers subtle brown tint */
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

st.write("Available columns:", df.columns.tolist())

x = st.selectbox("X-axis (group by)", df.columns)
y = st.selectbox("Y-axis (value to sum)", df.columns)

# 🟢 Debug print
st.write("X selected:", x)
st.write("Y selected:", y)
st.write("Sample data:", df[[x, y]].head())

# Safe check
if df[x].ndim != 1:
    st.error(f"🚫 Selected index `{x}` is not 1D!")
else:
    pivot = pd.pivot_table(df, index=x, values=y, aggfunc='sum')
    st.dataframe(pivot)

    chart = alt.Chart(pivot.reset_index()).mark_bar().encode(
        x=x,
        y=y
    )
    st.altair_chart(chart, use_container_width=True)
