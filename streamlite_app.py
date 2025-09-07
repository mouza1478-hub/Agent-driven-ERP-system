import streamlit as st
import requests
import json
import sys
import os 
from datetime import datetime

# Import domain agents (must exist in Agents folder)
from agents.sales_agent import executor as sales_executor
from agents.finance_agent import executor as finance_executor
from agents.inventory_agent import executor as inventory_executor
from agents.analytics_agent import executor as analytics_executor


# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --------------------------
# Streamlit Page Settings
# --------------------------
st.set_page_config(
    page_title="Agent-Driven ERP",
    page_icon="🤖",
    layout="wide"
)

# --------------------------
# Custom CSS
# --------------------------
st.markdown(
    """
    <style>
        /* Main Header Styling */
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Card container */
        .agent-card {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        }

        .agent-card:hover {
            transform: scale(1.02);
            border-color: #2E86C1;
        }

        /* Card header */
        .agent-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1B4F72;
            margin-bottom: 8px;
        }

        /* Card text */
        .agent-desc {
            font-size: 1rem;
            color: #444;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# App Header
# --------------------------
st.markdown("<div class='main-header'>🤖 Agent-Driven ERP Dashboard</div>", unsafe_allow_html=True)

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("🔍 Select Agent")
agent_choice = st.sidebar.radio(
    "Choose an agent:",
    ["Sales Agent", "Finance Agent", "Inventory Agent", "Analytics Agent"]
)

# --------------------------
# Agent Cards
# --------------------------
st.markdown(
    """
    <div class="agent-card">
        <div class="agent-title">📊 Sales Agent</div>
        <div class="agent-desc">Get insights into top customers, revenue trends, and sales by status.</div>
    </div>
    
    <div class="agent-card">
        <div class="agent-title">💰 Finance Agent</div>
        <div class="agent-desc">Generate summaries of income, expenses, and profit margins.</div>
    </div>
    
    <div class="agent-card">
        <div class="agent-title">📦 Inventory Agent</div>
        <div class="agent-desc">Track stock levels, restock alerts, and product movement.</div>
    </div>
    
    <div class="agent-card">
        <div class="agent-title">📈 Analytics Agent</div>
        <div class="agent-desc">Perform deep analytics on sales, customers, and performance KPIs.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Agent Executor Function
# --------------------------
def run_agent(agent_executor, query):
    try:
        result = agent_executor.invoke({"user_input": query})
        return result.get("output", "No output generated.")
    except Exception as e:
        return f"❌ Error: {str(e)}"


# --------------------------
# Main Content Area
# --------------------------
st.subheader(f"💡 {agent_choice}")

user_query = st.text_input(f"Ask something to {agent_choice}:", "")

if st.button("Run Query"):
    if user_query.strip():
        with st.spinner("Processing..."):
            if agent_choice == "Sales Agent":
                response = run_agent(sales_executor, user_query)
            elif agent_choice == "Finance Agent":
                response = run_agent(finance_executor, user_query)
            elif agent_choice == "Inventory Agent":
                response = run_agent(inventory_executor, user_query)
            elif agent_choice == "Analytics Agent":
                response = run_agent(analytics_executor, user_query)
            else:
                response = "Invalid agent selected."
        st.success("✅ Done!")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a query first.")



