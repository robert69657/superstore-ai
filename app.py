import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("🛒 Superstore Analytics & Chatbot")

@st.cache_data
def load_data():
    return pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

df = load_data()

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Dataset", "Chatbot"])

if page == "Dashboard":
    st.header("📊 Sales Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
    col2.metric("Total Profit", f"${df['Profit'].sum():,.2f}")

    sales_by_category = df.groupby("Category")["Sales"].sum().reset_index()
    fig = px.bar(sales_by_category, x="Category", y="Sales", title="Sales by Category")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Dataset":
    st.header("📋 Superstore Dataset")
    st.dataframe(df.head(50), use_container_width=True)

elif page == "Chatbot":
    st.header("🤖 Superstore AI Chatbot")
    st.info("Run the chatbot using the command below:")
    st.code("streamlit run chatbot.py")
