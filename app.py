import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sample_sales_data.csv")
    return df

df = load_data()

# Sidebar navigation
st.sidebar.title("📊 Multi-Dashboard Navigation")
dashboard = st.sidebar.radio("Choose Dashboard:", 
    ["Overview", "Sales by Product", "Sales by Region", "Time-Series", "Customers"])

# Dashboard 1: Overview
if dashboard == "Overview":
    st.title("📊 Sales Overview")
    st.metric("Total Revenue", f"${df['Revenue'].sum():,.2f}")
    st.metric("Total Quantity Sold", f"{df['Quantity'].sum():,}")
    st.metric("Unique Customers", df['CustomerID'].nunique())

# Dashboard 2: Sales by Product
elif dashboard == "Sales by Product":
    st.title("🛒 Sales by Product")
    product_sales = df.groupby("Product")["Revenue"].sum().reset_index()
    fig = px.bar(product_sales, x="Product", y="Revenue", title="Revenue by Product", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# Dashboard 3: Sales by Region
elif dashboard == "Sales by Region":
    st.title("🌍 Sales by Region")
    if "Region" in df.columns:
        region_sales = df.groupby("Region")["Revenue"].sum().reset_index()
        fig = px.pie(region_sales, names="Region", values="Revenue", title="Revenue Share by Region")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'Region' column found in dataset.")

# Dashboard 4: Time-Series
elif dashboard == "Time-Series":
    st.title("📈 Time-Series Analysis")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        time_sales = df.groupby("Date")["Revenue"].sum().reset_index()
        fig = px.line(time_sales, x="Date", y="Revenue", title="Revenue Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'Date' column found in dataset.")

# Dashboard 5: Customers
elif dashboard == "Customers":
    st.title("👥 Customer Insights")
    if "CustomerID" in df.columns:
        top_customers = df.groupby("CustomerID")["Revenue"].sum().nlargest(10).reset_index()
        fig = px.bar(top_customers, x="CustomerID", y="Revenue", title="Top 10 Customers", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'CustomerID' column found in dataset.")
