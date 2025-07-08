import streamlit as st
import pandas as pd

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Sidebar gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom right, #5D4037, #8D6E63);
}

/* Sidebar text: white */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Main area: white */
.stApp {
    background-color: #ffffff;
}

/* Main text: dark brown */
.stApp, .stApp * {
    color: #4E342E;
}

/* Metric containers */
div[data-testid="metric-container"] {
    background: rgba(93, 64, 55, 0.05);
    border-radius: 8px;
    padding: 10px;
}

/* File uploader */
section[data-testid="stFileUploader"] label div {
    background-color: #5D4037;
    color: #ffffff;
    border-radius: 5px;
    padding: 6px 12px;
}

/* Buttons — both kinds */
button[kind="secondary"], button[kind="primary"] {
    background-color: #5D4037 !important;
    color: #ffffff !important;
    border: none !important;
}

button[kind="secondary"]:hover, button[kind="primary"]:hover {
    background-color:#ffffff!important;
    color: #ffffff !important;
}

    </style>
    """,
    unsafe_allow_html=True
)

st.title("📂 Load Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state['raw_df'] = df
    st.write("✅ File uploaded.")
    st.dataframe(df.head())
else:
    st.info("Upload your CSV or try the sample below:")

    if st.button("📄 Load Sample Data"):
        df = pd.read_csv("data/sample.csv")
        st.session_state['raw_df'] = df
        st.dataframe(df.head())
