import streamlit as st
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Superstore AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# LOAD ENV + OPENAI
# ===============================
load_dotenv(find_dotenv())
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

st.write("API KEY LOADED:", bool(OPENAI_KEY))


USE_AI = False
client = None

if OPENAI_KEY:
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        USE_AI = True
    except:
        USE_AI = False

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

df = load_data()

# ===============================
# HEADER
# ===============================
st.markdown("""
<div class="main-header">
    <h1>🛒 Superstore AI Assistant</h1>
    <p>Analyze sales data intelligently</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("## 🎛 Control Panel")

    if USE_AI:
        st.success("✅ OpenAI Connected")
        st.caption(f"Key: {OPENAI_KEY[:8]}...")
    else:
        st.warning("⚠ OpenAI Disabled")

    st.markdown("---")
    show_dataset = st.checkbox("📊 Show Dataset", False)
    use_ai = st.checkbox("🤖 Enable AI Answer", USE_AI)

    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.markdown("""
    - Total sales  
    - Total profit  
    - Top category  
    - Sales by region  
    - Business insights  
    """)

# ===============================
# RULE-BASED CHATBOT
# ===============================
def simple_chatbot(question):
    q = question.lower()

    if "total sales" in q:
        return f"💰 Total Sales: ${df['Sales'].sum():,.2f}"

    if "total profit" in q:
        return f"📈 Total Profit: ${df['Profit'].sum():,.2f}"

    if "top category" in q:
        top = df.groupby("Category")["Sales"].sum().idxmax()
        return f"🏆 Top Category: {top}"

    if "sales by region" in q:
        return df.groupby("Region")["Sales"].sum().to_frame("Sales")

    if "insight" in q or "summary" in q:
        return (
            f"📊 Business Summary:\n"
            f"- Total Sales: ${df['Sales'].sum():,.2f}\n"
            f"- Total Profit: ${df['Profit'].sum():,.2f}\n"
            f"- Best Category: {df.groupby('Category')['Sales'].sum().idxmax()}"
        )

    return "❌ I can answer sales, profit, category, region, and insights."

# ===============================
# AI CHATBOT (OPENAI)
# ===============================
def ai_chatbot(question):
    prompt = f"""
You are a business data analyst.
Answer ONLY using the dataset below.

DATA SAMPLE:
{df.head(40).to_string()}

QUESTION:
{question}

Answer clearly and briefly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze Superstore sales data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# ===============================
# TABS
# ===============================
tab1, tab2 = st.tabs(["💬 Chatbot", "📊 Data Explorer"])

with tab1:
    query = st.text_input(
        "Ask something about the Superstore data",
        placeholder="e.g. What is the total sales?"
    )

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("💰 Total Sales"):
        query = "total sales"
    if col2.button("📈 Total Profit"):
        query = "total profit"
    if col3.button("🏆 Top Category"):
        query = "top category"
    if col4.button("🌍 Sales by Region"):
        query = "sales by region"

    if query:
        st.markdown("### 🔍 Result")

        result = simple_chatbot(query)

        if isinstance(result, pd.DataFrame):
            st.dataframe(result, use_container_width=True)
        else:
            st.success(result)

        if use_ai and USE_AI:
            st.markdown("### 🤖 AI Explanation")
            try:
                st.info(ai_chatbot(query))
            except Exception as e:
                st.error("❌ OpenAI Error. Check API key or billing.")

with tab2:
    if show_dataset:
        st.dataframe(df.head(50), use_container_width=True)
    else:
        st.info("Enable dataset view from sidebar")

# ===============================
# FOOTER
# ===============================
st.markdown("""
<hr>
<div style="text-align:center;color:gray;">
    🛒 Superstore AI Assistant — Streamlit App
</div>
""", unsafe_allow_html=True)
