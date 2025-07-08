import streamlit as st
import pandas as pd
import time
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

st.title("📝 Query + Views + Rollup")

if 'conn' not in st.session_state:
    st.warning("Run ETL first.")
    st.stop()

conn = st.session_state['conn']

st.subheader("✅ Auto JOIN Example")

dims = st.session_state['dimensions']
dim = st.selectbox("Choose dimension", [d['name'] for d in dims])

d = next(d for d in dims if d['name'] == dim)

join_pk = d['pk'] or 'id'
join_fk = d['fk'] or 'id'

st.write(f"PK: `{join_pk}` | FK: `{join_fk}`")

example = f"""
SELECT f.*, d.* 
FROM fact_table f 
JOIN {dim} d 
ON f.{join_fk} = d.{join_pk}
"""

st.code(example)

query = st.text_area("Your SQL:", example)

if st.button("Run Query"):
    start = time.time()
    try:
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)
        st.success(f"✅ Done in {time.time() - start:.3f} sec.")
    except Exception as e:
        st.error(e)

st.subheader("✅ Create Materialized View")
mv_name = st.text_input("View name", "mv_example")
mv_query = st.text_area("View SQL", f"CREATE TABLE {mv_name} AS {example}")

if st.button("Create View"):
    try:
        conn.execute(mv_query)
        st.success(f"✅ View `{mv_name}` created.")
    except Exception as e:
        st.error(e)

if st.button("Drop View"):
    try:
        conn.execute(f"DROP TABLE IF EXISTS {mv_name}")
        st.success(f"✅ View `{mv_name}` dropped.")
    except Exception as e:
        st.error(e)
