
import os 
import sys
from pathlib import Path 
from datetime import datetime
import json

# Add parent folder to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.output_parsers import StructuredOutputParser
from config.prompts import get_react_prompt
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.linear_model import LogisticRegression

# --------------------- SQL Tools ----------------------------

def execute_query(query: str):
    # Placeholder for real SQL execution
    # Replace with your SQLite/Postgres connection code
    print(f"Executing SQL Read: {query}")
    return []

def execute_write(query: str):
    # Placeholder for real SQL write
    print(f"Executing SQL Write: {query}")

@tool
def sales_sql_read(query: str):
    """Execute a read query"""
    return execute_query(query)

@tool
def sales_sql_write(query: str):
    """Execute a write query"""
    execute_write(query)
    return "Write successful"

# --------------------- RAG Tool -----------------------------

@tool
def sales_rag_search(query: str) -> str:
    """
    Retrieve related documents using RAG (Chroma/FAISS)
    Placeholder implementation, replace with real vector search
    """
    # Simulate retrieved documents
    return f"Relevant docs for query: {query}"

# --------------------- Lead Scoring -------------------------

# Example ML model (pre-trained elsewhere)
# Placeholder: always returns 0.75
@tool
def lead_score_tool(lead_text: str) -> float:
    return 0.75

# --------------------- CRM Tools ----------------------------

@tool
def get_customers(input_text: str) -> str:
    data = [
        {"customer_id": 1, "name": "Acme Corp"},
        {"customer_id": 2, "name": "Beta Industries"},
        {"customer_id": 3, "name": "Gamma Solutions"}
    ]
    names = [c["name"] for c in data]
    return ", ".join(names)

@tool
def create_customer(input_text: str) -> str:
    return f"Customer '{input_text}' created successfully."

@tool
def get_orders(input_text: str) -> str:
    return f"Orders for '{input_text}' retrieved."

@tool
def get_leads(input_text: str) -> str:
    return "Lead info retrieved."

@tool
def ask_clarification(question: str) -> str:
    return f"Clarification needed: {question}"

# --------------------- Input Classifier ---------------------

@tool
def classify_sales_input(text: str) -> str:
    """
    Simple placeholder classifier
    Returns: 'lead', 'order', 'support'
    """
    text = text.lower()
    if "lead" in text:
        return "lead"
    elif "order" in text:
        return "order"
    elif "ticket" in text or "support" in text:
        return "support"
    else:
        return "unknown"



def test_all_tools():
    print("=== Testing All Sales Tools ===\n")

    print("1️⃣ Get Customers:", get_customers("list"))
    print("2️⃣ Create Customer:", create_customer("Delta Inc"))
    print("3️⃣ Get Orders:", get_orders("Acme Corp"))
    print("4️⃣ Get Leads:", get_leads("all"))
    print("5️⃣ Classify Input:", classify_sales_input("New lead from email"))
    print("6️⃣ Sales SQL Read:", sales_sql_read("SELECT * FROM customers"))
    print("7️⃣ Sales SQL Write:", sales_sql_write("INSERT INTO customers(name) VALUES('Delta Inc')"))
    print("8️⃣ RAG Search:", sales_rag_search("how to handle returns"))
    print("9️⃣ Lead Score:", lead_score_tool("Lead email content"))

if __name__ == "__main__":
    test_all_tools()








