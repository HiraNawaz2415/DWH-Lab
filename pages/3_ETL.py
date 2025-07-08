import streamlit as st
import sqlite3
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
st.title("⚙️ ETL — Load to Data Warehouse")

st.write("""
This step **loads your cleaned & modeled data into the Data Warehouse** (DW).  
You’ll see how a **fact table**, **dimensions**, and any **sub-dimensions** are saved.
""")

# Make sure fact table is ready
if 'fact_table' not in st.session_state:
    st.warning("⚠️ Please define your schema first (Fact & Dimensions).")
    st.stop()

# ✅ Use file DB so data persists across pages
conn = sqlite3.connect("dw_lab.db", check_same_thread=False)

# ✅ 1️⃣ Load FACT table
st.subheader("✅ 1️⃣ Fact Table")
fact = st.session_state['fact_table']

if fact is not None and not fact.empty:
    fact.to_sql('fact_table', conn, index=False, if_exists='replace')
    st.success(f"✔️ Fact table saved as `fact_table` with {len(fact)} rows and {len(fact.columns)} columns.")
    if st.checkbox("🔍 Show Fact Table Sample"):
        st.dataframe(fact.head())
else:
    st.warning("⚠️ Fact table is empty! Please check your schema.")

# ✅ 2️⃣ Load DIMENSIONS
st.subheader("✅ 2️⃣ Dimensions")
for d in st.session_state['dimensions']:
    dim_df = d['table']
    dim_name = d['name']

    st.write(f"**Dimension:** `{dim_name}`")
    if dim_df is not None and not dim_df.empty:
        dim_df.to_sql(dim_name, conn, index=False, if_exists='replace')
        st.success(f"✔️ Dimension `{dim_name}` saved with {len(dim_df)} rows.")
        if st.checkbox(f"🔍 Show `{dim_name}`", key=dim_name):
            st.dataframe(dim_df.head())
    else:
        st.warning(f"⚠️ Dimension `{dim_name}` is empty! Please check your selected columns.")

    # ✅ 3️⃣ If this dimension has a sub-dimension
    if d['sub_dim']:
        sub = d['sub_dim']
        sub_name = sub['name']
        sub_table = st.session_state['raw_df'][sub['columns']].drop_duplicates()

        st.write(f"↳ Sub-dimension: `{sub_name}`")
        if sub_table is not None and not sub_table.empty:
            sub_table.to_sql(sub_name, conn, index=False, if_exists='replace')
            st.success(f"✔️ Sub-dimension `{sub_name}` saved with {len(sub_table)} rows.")
            if st.checkbox(f"🔍 Show `{sub_name}`", key=sub_name):
                st.dataframe(sub_table.head())
        else:
            st.warning(f"⚠️ Sub-dimension `{sub_name}` is empty! Double-check its source columns.")

# ✅ Save connection for other pages
st.session_state['conn'] = conn

st.info("""
✅ **ETL Complete!**  
Your **Fact**, **Dimensions**, and **Sub-dimensions** are now loaded in `dw_lab.db`.  
You can query this data or create materialized views in the **next pages**.
""")
