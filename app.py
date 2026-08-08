
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Integrated Business Analytics",
    page_icon="📊",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "data" / "cleaned"
RAW = ROOT / "data" / "raw"

def load_data():
    sales_file = CLEAN / "sales_cleaned.csv"
    marketing_file = CLEAN / "marketing_cleaned.csv"
    hr_file = CLEAN / "hr_cleaned.csv"

    if not (sales_file.exists() and marketing_file.exists() and hr_file.exists()):
        st.warning("Cleaned files not found. Loading raw data. Run: python scripts/data_cleaning.py")
        sales = pd.read_csv(RAW / "sales.csv", parse_dates=["Order_Date"])
        marketing = pd.read_csv(RAW / "marketing.csv")
        hr = pd.read_csv(RAW / "hr.csv")
    else:
        sales = pd.read_csv(sales_file, parse_dates=["Order_Date"])
        marketing = pd.read_csv(marketing_file)
        hr = pd.read_csv(hr_file)
    return sales, marketing, hr

sales, marketing, hr = load_data()

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Choose analysis",
    ["🏠 Overview", "🛒 Sales Analytics", "📢 Marketing Analytics", "👥 HR Analytics", "🧹 Data Quality"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Integrated Business Analytics Project")
st.sidebar.caption("Python • Pandas • Streamlit • Plotly")

# ---------------- Overview ----------------
if page == "🏠 Overview":
    st.title("📊 Integrated Business Analytics Dashboard")
    st.write("A single decision-support dashboard combining Sales, Marketing and HR analytics.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"₹{sales['Sales'].sum():,.0f}")
    c2.metric("Total Profit", f"₹{sales['Profit'].sum():,.0f}")
    c3.metric("Marketing Revenue", f"₹{marketing['Revenue'].sum():,.0f}")
    attrition = (hr["Attrition"].eq("Yes").mean() * 100)
    c4.metric("Employee Attrition", f"{attrition:.1f}%")

    st.subheader("Project workflow")
    st.markdown("""
    **Raw Data → Python/Pandas Cleaning → EDA → Interactive Dashboards → Business Insights**

    This project demonstrates the four internship tasks:
    - **Task 01:** Excel-style sales dashboard and KPI analysis
    - **Task 02:** Data cleaning and preparation with Pandas
    - **Task 03:** Interactive visualization with filters and dashboards
    - **Task 04:** Marketing EDA and ROI-based recommendations
    """)

    monthly = sales.groupby(sales["Order_Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly["Month"] = monthly["Order_Date"].astype(str)
    fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Sales ----------------
elif page == "🛒 Sales Analytics":
    st.title("🛒 Sales & Profit Analytics")

    regions = st.multiselect("Region", sorted(sales["Region"].unique()), default=sorted(sales["Region"].unique()))
    cats = st.multiselect("Category", sorted(sales["Category"].unique()), default=sorted(sales["Category"].unique()))

    df = sales[sales["Region"].isin(regions) & sales["Category"].isin(cats)].copy()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
    c2.metric("Total Profit", f"₹{df['Profit'].sum():,.0f}")
    c3.metric("Quantity", f"{df['Quantity'].sum():,.0f}")
    margin = (df["Profit"].sum()/df["Sales"].sum()*100) if df["Sales"].sum() else 0
    c4.metric("Profit Margin", f"{margin:.1f}%")

    col1, col2 = st.columns(2)

    with col1:
        cat = df.groupby("Category", as_index=False)[["Sales","Profit"]].sum()
        fig = px.bar(cat, x="Category", y="Sales", title="Sales by Category", text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        reg = df.groupby("Region", as_index=False)[["Sales","Profit"]].sum()
        fig = px.bar(reg, x="Region", y="Profit", title="Profit by Region", text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)

    monthly = df.groupby(df["Order_Date"].dt.to_period("M"))[["Sales","Profit"]].sum().reset_index()
    monthly["Month"] = monthly["Order_Date"].astype(str)
    fig = px.line(monthly, x="Month", y=["Sales","Profit"], markers=True, title="Sales and Profit Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top and low-performing products")
    product = df.groupby("Product", as_index=False)[["Sales","Profit"]].sum().sort_values("Profit", ascending=False)
    st.dataframe(product, use_container_width=True)

    st.info("Business question: Which categories, regions and products contribute most to sales and profit?")

# ---------------- Marketing ----------------
elif page == "📢 Marketing Analytics":
    st.title("📢 Marketing Campaign EDA")

    channels = st.multiselect(
        "Marketing Channel",
        sorted(marketing["Channel"].unique()),
        default=sorted(marketing["Channel"].unique())
    )
    df = marketing[marketing["Channel"].isin(channels)].copy()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Spend", f"₹{df['Spend'].sum():,.0f}")
    c2.metric("Revenue", f"₹{df['Revenue'].sum():,.0f}")
    c3.metric("Conversions", f"{df['Conversions'].sum():,.0f}")
    total_spend = df["Spend"].sum()
    total_rev = df["Revenue"].sum()
    roi = ((total_rev-total_spend)/total_spend*100) if total_spend else 0
    c4.metric("Overall ROI", f"{roi:.1f}%")

    col1, col2 = st.columns(2)

    with col1:
        channel = df.groupby("Channel", as_index=False)[["Spend","Revenue"]].sum()
        fig = px.bar(channel, x="Channel", y=["Spend","Revenue"], barmode="group",
                     title="Spend vs Revenue by Channel")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        roi_df = df.groupby("Channel", as_index=False).agg(
            Spend=("Spend","sum"), Revenue=("Revenue","sum")
        )
        roi_df["ROI"] = ((roi_df["Revenue"]-roi_df["Spend"])/roi_df["Spend"]*100).fillna(0)
        fig = px.bar(roi_df.sort_values("ROI", ascending=False),
                     x="Channel", y="ROI", title="ROI by Channel", text_auto=".1f")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df, x="Spend", y="Revenue", size="Conversions",
                     color="Channel", hover_data=["Campaign"],
                     title="Ad Spend vs Revenue")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Channel performance")
    st.dataframe(roi_df.sort_values("ROI", ascending=False), use_container_width=True)

    best = roi_df.sort_values("ROI", ascending=False).iloc[0]
    st.success(
        f"Recommendation: **{best['Channel']}** has the highest ROI in the current dataset "
        f"({best['ROI']:.1f}%). Consider prioritizing this channel after validating campaign quality and scale."
    )

# ---------------- HR ----------------
elif page == "👥 HR Analytics":
    st.title("👥 HR Analytics & Attrition")

    depts = st.multiselect(
        "Department",
        sorted(hr["Department"].unique()),
        default=sorted(hr["Department"].unique())
    )
    df = hr[hr["Department"].isin(depts)].copy()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", f"{len(df):,}")
    attr = df["Attrition"].eq("Yes").mean()*100
    c2.metric("Attrition Rate", f"{attr:.1f}%")
    c3.metric("Avg Satisfaction", f"{df['Job_Satisfaction'].mean():.2f}/5")
    c4.metric("Avg Salary", f"₹{df['Salary'].mean():,.0f}")

    col1, col2 = st.columns(2)

    with col1:
        dept = df.groupby("Department", as_index=False).size()
        dept.columns = ["Department","Employees"]
        fig = px.bar(dept, x="Department", y="Employees", title="Employees by Department")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        attr_dept = pd.crosstab(df["Department"], df["Attrition"], normalize="index")*100
        attr_dept = attr_dept.reset_index()
        if "Yes" in attr_dept.columns:
            fig = px.bar(attr_dept, x="Department", y="Yes",
                         title="Attrition Rate by Department", text_auto=".1f")
            st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df, x="Job_Satisfaction", y="Salary",
                     color="Attrition", size="Years_At_Company",
                     hover_data=["Department","Job_Role"],
                     title="Job Satisfaction vs Salary")
    st.plotly_chart(fig, use_container_width=True)

    factors = df.groupby("Job_Satisfaction", as_index=False)["Attrition"].apply(
        lambda x: (x == "Yes").mean()*100
    )
    factors.columns = ["Job_Satisfaction","Attrition_Rate"]
    st.subheader("Attrition by job satisfaction")
    st.dataframe(factors, use_container_width=True)

    st.info("Business question: Are low satisfaction, high workload and short tenure associated with higher attrition?")

# ---------------- Data Quality ----------------
else:
    st.title("🧹 Data Quality & Preparation")

    for name, df in [("Sales", sales), ("Marketing", marketing), ("HR", hr)]:
        st.subheader(name)
        q1, q2, q3 = st.columns(3)
        q1.metric("Rows", f"{len(df):,}")
        q2.metric("Columns", f"{len(df.columns):,}")
        q3.metric("Duplicate Rows", f"{df.duplicated().sum():,}")
        st.write("Missing values:")
        missing = df.isna().sum().reset_index()
        missing.columns = ["Column","Missing Values"]
        st.dataframe(missing, use_container_width=True)

st.markdown("---")
st.caption("Internship Project • Integrated Business Analytics & Decision Support System")
