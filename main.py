import streamlit as st
from fpdf import FPDF

# Page config
st.set_page_config(
    page_title="📦 Data Warehouse Lab",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
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

    /* Main content area: white */
    .stApp {
        background-color: #ffffff;
    }

    /* Main text: dark brown */
    .stApp, .stApp * {
        color: #4E342E;
    }

    /* Metric container styling */
    div[data-testid="metric-container"] {
        background: rgba(93, 64, 55, 0.05);
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title & intro
st.title("📦 Data Warehouse Lab — Star & Snowflake DW Practical")
st.markdown("""
Welcome! This lab lets you:
- Upload raw data
- Define **Star** / **Snowflake** schemas
- Create **fact** and **dimension** tables
- Simulate **ETL process**
- Write **JOIN** queries
- Create **materialized views**
- Do **OLAP aggregation & drill-down**
- Visualize pivots and dashboards
""")

# 📚 Theory Q&A
with st.expander("📖 **Data Warehouse Important Questions & Answers**"):
    st.markdown("""
**1️.What is a Fact Table?**  
Stores **quantitative data** (sales, revenue, etc.) and **foreign keys** to dimension tables.

---

**2️.What is a Dimension Table?**  
Stores **descriptive attributes** — e.g., Product, Customer, Time.

---

**3️.What is a Star Schema?**  
Central **fact table** connects directly to dimension tables — looks like a star.

---

**4️.What is a Snowflake Schema?**  
An extended star schema — dimension tables are **normalized** into sub-dimensions.

---

**5️.What is OLAP?**  
**Online Analytical Processing:** supports aggregation, drill-down, multi-dimensional queries.

---

**6️.What is OLTP?**  
**Online Transaction Processing:** handles daily transactions — fast & accurate.

---

**7️.What is ETL?**  
**Extract, Transform, Load:** extract data, clean/map it, load to DW.

---

**8️.What is Conceptual & Logical Design?**  
- **Conceptual:** high-level entities & relationships.
- **Logical:** details like tables, keys — not physical storage yet.

---

**9️.Life Cycle of DW?**  
Requirement ➜ Modeling ➜ ETL ➜ Implementation ➜ Testing ➜ Deployment ➜ Maintenance
""")

# ✅ PDF Download
def generate_dwh_qa_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Data Warehouse Important Questions & Answers", ln=True, align="C")

    qa = [
        ("1) What is a Fact Table?", "Stores quantitative data for analysis, such as sales, revenue, or cost."),
        ("2) What is a Dimension Table?", "Stores descriptive attributes to filter, group, and label facts."),
        ("3) What is a Star Schema?", "Central fact table connects directly to dimension tables — star shape."),
        ("4) What is a Snowflake Schema?", "Star schema with normalized dimensions forming branches."),
        ("5) What is OLAP?", "Supports complex queries, aggregation, multi-dimensional analysis."),
        ("6) What is OLTP?", "Handles daily transactions — bank, retail, orders."),
        ("7) What is ETL?", "Extract, Transform, Load process."),
        ("8) Conceptual & Logical Design?", "Conceptual: big picture. Logical: detail mapping of data structures."),
        ("9) Life Cycle of DW?", "Requirement -> Design -> ETL -> Implement -> Test -> Deploy -> Maintain.")
    ]

    for q, a in qa:
        pdf.multi_cell(0, 10, txt=f"{q}\n{a}\n")

    return pdf.output(dest='S').encode('latin1')

 # ✅ PDF download inside the expander
    if st.button("📄 Generate Q&A PDF"):
        pdf_bytes = generate_dwh_qa_pdf()
        st.download_button(
            label="⬇️ Download Q&A PDF",
            data=pdf_bytes,
            file_name="DWH_Questions_Answers.pdf",
            mime="application/pdf"
        )
st.title("📝 DWH Mini Quiz")

st.markdown("Check your knowledge on basic Data Warehouse concepts!")

# Track answers
with st.form("quiz_form"):
    q1 = st.radio("1️⃣ What does a Fact Table store?",
                  ["A) Descriptive attributes", "B) Quantitative data", "C) ER Diagrams"])

    q2 = st.radio("2️⃣ Which schema uses normalized dimensions?",
                  ["A) Star Schema", "B) Flat File", "C) Snowflake Schema"])

    q3 = st.radio("3️⃣ OLAP is used for?",
                  ["A) Real-time transactions", "B) Data backups", "C) Analytical queries & reporting"])

    q4 = st.radio("4️⃣ ETL stands for?",
                  ["A) Extract, Transform, Load", "B) Evaluate, Transfer, Learn", "C) Export, Test, Launch"])

    q5 = st.radio("5️⃣ OLTP is best described as?",
                  ["A) Complex reporting", "B) Transaction processing", "C) Data mining"])

    submitted = st.form_submit_button("✅ Submit Answers")

if submitted:
    score = 0

    if q1.startswith("B"):
        st.success("1️⃣ ✅ Correct! A Fact Table stores quantitative data.")
        score += 1
    else:
        st.error("1️⃣ ❌ Incorrect. The correct answer is: Quantitative data.")

    if q2.startswith("C"):
        st.success("2️⃣ ✅ Correct! Snowflake Schema uses normalized dimensions.")
        score += 1
    else:
        st.error("2️⃣ ❌ Incorrect. Correct answer: Snowflake Schema.")

    if q3.startswith("C"):
        st.success("3️⃣ ✅ Correct! OLAP is for analytical queries & reporting.")
        score += 1
    else:
        st.error("3️⃣ ❌ Incorrect. Correct answer: Analytical queries & reporting.")

    if q4.startswith("A"):
        st.success("4️⃣ ✅ Correct! ETL = Extract, Transform, Load.")
        score += 1
    else:
        st.error("4️⃣ ❌ Incorrect. Correct answer: Extract, Transform, Load.")

    if q5.startswith("B"):
        st.success("5️⃣ ✅ Correct! OLTP = Transaction processing.")
        score += 1
    else:
        st.error("5️⃣ ❌ Incorrect. Correct answer: Transaction processing.")

    st.info(f"**Your Final Score: {score}/5**")

    if score == 5:
        st.balloons()
        st.success("🎉 Perfect! You really know your DW basics!")
    elif score >= 3:
        st.info("👍 Good job! Keep practicing.")
    else:
        st.warning("📌 Review the theory and try again!")