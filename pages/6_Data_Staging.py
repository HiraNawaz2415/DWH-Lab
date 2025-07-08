import streamlit as st
import sqlite3
import pandas as pd

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Sidebar: brown gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom right, #5D4037, #8D6E63);
    }

    /* Sidebar text: white */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
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
st.title("🗄️ Data Staging Area — ETL Walkthrough")

# Check that user uploaded something
if 'raw_df' not in st.session_state:
    st.warning("⚠️ Please upload your raw CSV in the Upload page first.")
    st.stop()

# The uploaded DataFrame
df = st.session_state['raw_df']

# Use file DB so it persists across pages
conn = sqlite3.connect("staging_lab.db", check_same_thread=False)

st.subheader("✅ 1️⃣ Raw Stage")
st.write("""
**What happens:**  
We load your original uploaded data into a staging table **without any cleaning**.  
This is your raw source.
""")
df.to_sql("staging_raw", conn, index=False, if_exists="replace")
st.success(f"✔️ Raw table saved as `staging_raw` with {len(df)} rows.")

if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# 🧹 Clean Stage
st.subheader("✅ 2️⃣ Clean Stage")
st.write("""
**What happens:**  
We remove rows with **NULL / missing values**.  
This is your cleaned version, ready for light transformation.
""")
df_clean = df.dropna()
df_clean.to_sql("staging_clean", conn, index=False, if_exists="replace")
st.success(f"✔️ Clean table saved as `staging_clean` with {len(df_clean)} rows.")

if st.checkbox("Show Cleaned Data"):
    st.dataframe(df_clean)

# 🔄 Transform Stage
st.subheader("✅ 3️⃣ Transform Stage")
st.write("""
**What happens:**  
You can add simple derived columns — for example, convert an amount to USD.
""")

if 'Amount' in df_clean.columns:
    if st.checkbox("Add `Amount_USD` column"):
        usd_rate = st.number_input("USD Rate", min_value=0.0, value=1.0, step=0.01)
        df_clean["Amount_USD"] = df_clean["Amount"] * usd_rate
        st.success(f"✔️ `Amount_USD` added using rate: {usd_rate}")

df_clean.to_sql("staging_transformed", conn, index=False, if_exists="replace")
st.success(f"✔️ Transformed table saved as `staging_transformed` with {len(df_clean)} rows.")

if st.checkbox("Show Transformed Data"):
    st.dataframe(df_clean)

# Save for other pages
st.session_state['conn_staging'] = conn

st.info("✅ **Staging done!** You can now load this into your Data Warehouse in the next step.")
