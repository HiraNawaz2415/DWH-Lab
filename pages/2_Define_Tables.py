import streamlit as st
import graphviz
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
    input, textarea, select {
        color: #ffffff !important;
        background-color: #4E342E !important;
    }
    .stNumberInput input,
    .stTextInput input,
    .stSelectbox div div div,
    .stMultiSelect div div {
        color: #ffffff !important;
        background-color: #4E342E !important;
    }
    button {
        color: #ffffff !important;
    }
    label {
        color: #ffffff !important;
    }
    ::placeholder {
        color: #dddddd !important;
        opacity: 1;
    }
    div[data-testid="metric-container"] {
        background: rgba(93, 64, 55, 0.05);
        border-radius: 8px;
        padding: 10px;
    }
    /* Number input spinner arrows: Chrome/Edge/Safari */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        background: #ffffff !important;
    }
    /* Firefox: hide default spinner */
    input[type=number] {
        -moz-appearance: textfield;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🗂️ Define Fact & Dimensions (Star/Snowflake)")

if 'raw_df' not in st.session_state:
    st.warning("Upload data first.")
    st.stop()

df = st.session_state['raw_df']
st.dataframe(df.head())

st.subheader("✅ Choose Schema Type")
schema_type = st.radio("Schema Type", ["Star", "Snowflake"])

st.subheader("✅ Define Fact Table")
columns = df.columns.tolist()
fact_cols = st.multiselect("Fact Table Columns", columns, default=columns)

st.subheader("✅ Define Dimensions")
dimension_defs = []
num_dimensions = st.number_input("Number of Dimensions", min_value=1, max_value=5, value=1)

for i in range(num_dimensions):
    st.write(f"--- Dimension {i+1} ---")
    dim_name = st.text_input(f"Dimension {i+1} Name", value=f"dim_{i+1}")
    dim_cols = st.multiselect(f"Columns for {dim_name}", columns, key=f"dim_cols_{i}")
    dim_pk = st.selectbox(f"Primary Key for {dim_name}", dim_cols, key=f"dim_pk_{i}")
    fact_fk = st.selectbox(f"FK in Fact for {dim_name}", fact_cols, key=f"fact_fk_{i}")

    sub_dim = None
    if schema_type == "Snowflake":
        add_sub = st.checkbox(f"Add Sub-dimension for {dim_name}?", key=f"sub_{i}")
        if add_sub:
            sub_name = st.text_input(f"Sub-dimension Name", value=f"sub_{dim_name}")
            sub_cols = st.multiselect(f"Sub-dim Columns", columns, key=f"sub_cols_{i}")
            sub_pk = st.selectbox(f"Sub-dim PK", sub_cols, key=f"sub_pk_{i}")
            dim_fk = st.selectbox(f"FK in {dim_name} for sub-dim", dim_cols, key=f"dim_fk_{i}")
            sub_dim = {'name': sub_name, 'columns': sub_cols, 'pk': sub_pk, 'fk': dim_fk}

    dimension_defs.append({'name': dim_name, 'columns': dim_cols, 'pk': dim_pk, 'fk': fact_fk, 'sub_dim': sub_dim})

if st.button("Save Schema"):
    st.session_state['fact_table'] = df[fact_cols]
    st.session_state['dimensions'] = []
    for d in dimension_defs:
        d_table = df[d['columns']].drop_duplicates()
        st.session_state['dimensions'].append({'name': d['name'], 'table': d_table, 'pk': d['pk'], 'fk': d['fk'], 'sub_dim': d['sub_dim']})
    st.session_state['schema_type'] = schema_type
    st.success(f"{schema_type} Schema saved.")

if 'fact_table' in st.session_state:
    dot = "digraph G { Fact [shape=box, color=lightblue]; "
    for d in st.session_state['dimensions']:
        dot += f"{d['name']} [shape=ellipse, color=lightgreen]; Fact -> {d['name']} [label=\"{d['fk']} ➜ {d['pk']}\"];"
        if d['sub_dim']:
            s = d['sub_dim']
            dot += f"{s['name']} [shape=ellipse, color=lightyellow]; {d['name']} -> {s['name']} [label=\"{s['fk']} ➜ {s['pk']}\"];"
    dot += "}"
    st.graphviz_chart(dot)
