# -------------------- Sales Agent ---------------------------

import os 
import sys
from pathlib import Path 
import json


#Working with file and directory paths in a platform-independent manner
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.output_parsers import StructuredOutputParser
from config.llm import get_llm
from config.prompts import get_sales_prompt
from tools.database_tools import get_customers, create_customer, get_orders, get_leads, ask_clarification


# --------------------- Tools for Sales Agent ---------------------

@tool
def get_customers(input_text: str) -> str:
    """Fetch all customer info from the database"""
    # Simulated database response
    data = [
        {"customer_id": 1, "name": "Acme Corp", "email": "acme@example.com", "phone": "555-1212"},
        {"customer_id": 2, "name": "Beta Industries", "email": "beta@example.com", "phone": "555-3434"},
        {"customer_id": 3, "name": "Gamma Solutions", "email": "gamma@example.com", "phone": "555-5656"}
    ]
    # Extract names only
    names = [c["name"] for c in data]
    return ", ".join(names)

'''
@tool
def create_customer(input_text: str) -> str:
    """Add a new customer to the database"""
    return f"Customer '{input_text}' created successfully."

@tool
def get_orders(input_text: str) -> str:
    """Fetch all orders or order details for a customer"""
    return f"Orders for '{input_text}' retrieved."

@tool
def get_leads(input_text: str) -> str:
    """Fetch leads and opportunities from the CRM system"""
    return "Lead info retrieved."
@tool
def ask_clarification(question: str) -> str:
    """Prompt the user for clarification."""
    return f"Clarification needed: {question}" 
'''

# --------------------- Tools for Sales Agent ---------------------

SALES_TOOLS = [get_customers, create_customer, get_orders, get_leads, ask_clarification]

# ----------------------------- LLM -----------------------------
llm = get_llm()

# ----------------------------- Parser --------------------------
output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=[
        {"name": "Action", "description": "The name of the tool to call"},
        {"name": "Action Input", "description": "JSON input to the tool"}
    ]
)
# --------------------- Tool names for the prompt -----------------
tool_names = [tool.name for tool in SALES_TOOLS]  
#--------------------------- prompt -------------------------------------

prompt = get_sales_prompt()
# ----------------------- Building the Sales Agent -----------------

agent = create_react_agent(
    llm=llm,
    tools=SALES_TOOLS,
    prompt=prompt
)

# Verbose is handled by the executor
executor = AgentExecutor(
    agent=agent,
    tools=SALES_TOOLS,
    verbose=True,              # <-- this is where verbose goes now
    handle_parsing_errors=True,
    max_iteration=3,
    early_stopping_method="generate"
)

def main_smart_sales_agent():
    """
    Interactive Smart Sales Agent
    This agent interacts with users, routes requests to the right specialist,
    and provides sales-related insights using the centralized executor.
    """
    # Welcome message
    print("\n=== Smart Sales Agent Ready! ===")
    print("I can handle customer info, sales leads, orders, and analytics.")
    print("Examples of commands:")
    print(" - 'Show me customers'        -> Auto-routes to Sales Agent")
    print(" - 'Financial summary'        -> Auto-routes to Finance Agent")
    print(" - 'Check inventory'          -> Auto-routes to Inventory Agent")
    print(" - 'Sales report'             -> Auto-routes to Analytics Agent")
    print("Type 'quit', 'exit', or 'q' to exit.\n")

    while True:
        user_input = input("Sales Agent > ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Exiting Smart Router Agent. Goodbye!")
            break
        try:
            result = executor.invoke({"input": user_input})
            print(f"Smart Router Response: {result['output']}\n")
        except KeyboardInterrupt as e:
            print(f"Sales Agent shutting down")

# ------------------------------------ MAIN -----------------------------------------
if __name__ == "__main__":
    main_smart_sales_agent()
