# 📦 Data Warehouse Lab — Streamlit App

Welcome to the **Data Warehouse Practical Lab**!  
This Streamlit app helps students understand **Data Warehousing** concepts practically — from data staging to Star/Snowflake schemas, ETL, OLAP, dashboards, queries, and more.

---

## 🚀 Features

✅ Upload raw CSV data  
✅ Stage data (clean, transform)  
✅ Design **Star** and **Snowflake** schemas  
✅ Create **Fact** and **Dimension** tables  
✅ Perform **ETL** (Extract, Transform, Load) steps  
✅ Write **JOIN queries** and test PK/FK logic  
✅ Create **Materialized Views**  
✅ Run **OLAP aggregations** and **drill-down**  
✅ Generate **Pivot Tables**  
✅ Interactive **Dashboards & Reports**  
✅ Download **Q&A PDF** for revision  
✅ Take a **Mini Quiz** to test your knowledge

---

## 📂 Project Structure

📦 datawarehouse-lab/
│
├── 📂 pages/
│ ├── 1_📂_Load_Data.py
│ ├── 2_📊_Schema_Definition.py
│ ├── 3_⚙️_ETL.py
│ ├── 4_🧩_Query_Views_Rollup.py
│ ├── 5_📈_Visualize.py
│ ├── 6_📝_Mini_Quiz.py
│
├── 📄 main.py # Home page + Theory + PDF Download
├── 📂 data/
│ ├── sample.csv # Optional sample dataset
│
└── requirements.txt


---

## ⚙️ Requirements

- Python >= 3.8  
- `streamlit`
- `pandas`
- `altair`
- `fpdf`
- `sqlite3` (built-in)

---

## 📥 Installation

1️⃣ Clone this repo:
```bash
git clone https://github.com/YOUR_USERNAME/datawarehouse-lab.git
cd datawarehouse-lab
