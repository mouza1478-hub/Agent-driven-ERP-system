

# Router / Orchestrator Agent (LangChain + SQLite + RAG-ready)
# This is the  Router/Orchestrator Agent that will be connected with four different agents 
# based on the query of the user: Sales/Finance/Inventory/Analytical


'''
Features:
- Full DB initialization (users seeded, approvals, tool_calls, conversations, messages, saved_reports)
- ConversationBufferWindowMemory(k=5)
- LLM-based routing (returns JSON with domain + needs_approval), with fallback rule-based classifier
- Domain agents: Sales, Finance, Inventory, Analytics (simple SQL + RAG behavior)
- Logging to tool_calls/messages/approvals
- Graceful fallback when vector DB or embeddings not available
'''

# ------------------------------- IMPORTS ------------------------------------------
import os 
import sys
from dotenv import load_dotenv #secure API key
from pathlib import Path 
import sqlite3

# Load environment variables for API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Working with file and directory paths in a platform-independent manner
sys.path.insert(0, str(Path(__file__).parent.parent))


# LangChain imports
from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from config.llm import get_llm
from config.prompts import get_react_promp


# Import domain agents (must exist in Agents folder)
'''from agents.sales_agent import executor as sales_executor
from agents.finance_agent import executor as finance_executor
from agents.inventory_agent import executor as inventory_executor
from agents.analytics_agent import executor as analytics_executor'''

#--------------------------------- DATABASE HELPER --------------------------------------
#  ----- Get Connected with you DB file rep.db and explore its content for logging/registry tool
db_path = "erp.db"

def get_connected():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(db_path)

def get_table_names():
  """Return a list of table names in the SQLite database."""
  try:
        conn = get_connected()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
  except Exception as e:
        return [f"Error fetching tables: {str(e)}"]

# ---------------------------- DOMAIN TOOLS ----------------------------------------
# Each tool wraps a domain executor and is visible to the LLM
# Think -> Decide tool -> act(Call tool) ->observe ->answer
#It represent the actions that my agent can perform , will be read by the llm through calling

@tool
def excute_with_sales_agent(user_request:str) -> str: #User quesry as string and returns string
    """
    Excute a request using the Sales Agent for customer, order, and lead managment.
    Input: user's request/question about sales, customers, orders'
    """
    try:
        print(f"Your request is being sent to the Sales Agent: {user_request}")
        result = sales_executor.invoke({"input": user_request})
        return f"Sales Agent Response:{result['output']}"
    except Exception as e:
        return f"Sales Agent error: {str(e)}"
@tool    
def excute_with_finance_agent(user_request:str) -> str: #User quesry as string and returns string
    """
    Excute a request using the Finance Agent for financial data and accounting. 
    Input: user's request/question about finances, invoices, payments, or accounting
    """
    try:
        print(f"Your request is being sent to the Finance Agent: {user_request}")
        result = finance_executor.invoke({"input": user_request})
        return f"Finance Agent Response:{result['output']}"
    except Exception as e:
        return f"Finance Agent error: {str(e)}"
@tool  
def excute_with_inventory_agent(user_request:str) -> str: 
    """
    Excute a request using the Inventort Agent for stock and product management. 
    Input: user's request/question about inventory, stock levels, or products
    """
    try:
        print(f"Your request is being sent to the Inventory Agent: {user_request}")
        result = inventory_executor.invoke({"input": user_request})
        return f"Inventory Agent Response:{result['output']}"
    except Exception as e:
        return f"Inventory Agent error: {str(e)}"
@tool
def excute_with_analytics_agent(user_request:str) -> str: 
    """
    Excute a request using the Analytics Agent for reports and business intelligence. 
    Input: user's request/question about analytics, reports, or business insights
    """
    try:
        print(f"Your request is being sent to the Analytics Agent: {user_request}")
        result = analytics_executor.invoke({"input": user_request})
        return f"Analytics Agent response:{result['output']}"
    except Exception as e:
        return f"Analytics Agent error: {str(e)}"
    
# --------------------------- CLASSIFIER & ROUTER -----------------------------
@tool
def classify_and_route(user_request: str) -> str:
    """
    Automatically classify user request and route it to the CORRECT agent BASED ON KEYWORDS.
    Input: user's request/question
    """
    request_lower = user_request.lower() # To avoid case-insensitive keyword matching

    # Keywords for each domain
    sales_keywords = [
    "customer", "lead", "prospect", "order", "purchase", "ticket",
    "crm", "client", "quote", "deal", "support", "follow-up"
]
    finance_keywords = [
    "invoice", "billing", "payment", "refund", "transaction", "ledger",
    "account", "policy", "budget", "cashflow", "expense", "tax", "anomaly"
]
    inventory_keywords = [
    "inventory", "stock", "warehouse", "supplier", "delivery", "supply",
    "purchase order", "po", "receipt", "shipment", "logistics", "forecast", "restock"
]
    analytics_keywords = [
    "report", "kpi", "metric", "dashboard", "analytics", "performance",
    "trend", "statistics", "sql", "chart", "visualization", "summary", "insight"
]

# Count keyword matches
    scores = {
    'sales': sum(1 for kw in sales_keywords if kw in request_lower),
    'finance': sum(1 for kw in finance_keywords if kw in request_lower),
    'inventory': sum(1 for kw in inventory_keywords if kw in request_lower),
    'analytics': sum(1 for kw in analytics_keywords if kw in request_lower) }

# Select domain with highest score
    best_domain = max(scores.items(), key =lambda x: x[1])
    if best_domain[1] == 0:
        return f"I can help you with various ERP tasks"
    
# Route for selection of the appropriate agent
    domain = best_domain[0]
    confidence = best_domain[1]
    print(f"auto routing to {domain} agent (confidence :{confidence} keywor matches)")

    if domain == 'sales':
        return excute_with_sales_agent(user_request)
    elif domain == 'finance':
        return excute_with_finance_agent(user_request)
    if domain == 'inventory':
        return excute_with_inventory_agent(user_request)
    if domain == 'analytics':
        return excute_with_analytics_agent(user_request)
    else:
        return f"Unable to route to appropriate agent. Be more specific."
    
# ---------------------------- SYSTEM INFO TOOL --------------------------
@tool
def get_system_info() -> str:
    """
    Get information about the ERP system and available agents.
    No input required.
    """
    try:
        tables = get_table_names()
        info = {
            "system": "Smart Agentic ERP System",
            "available_agents":[
                "Sales Agent - Customer management, orders, leads (auto-routed)"
                "Finance Agent - Invoices, payments, accounting (auto-routed)"
                "Inventory Agent - Stock managment, products (auto-routed)"
                "Analutics Agent - Reports and business intelligence (auto-routed)"
                ],
                "database_tables":len(tables),
                "key_tables":["customers", "orders", "products", "invoices","leads","stock"]

        }
        return f"""
Smart ERP System Information:
-Systems:{info['system']}
-Database Tables: {info['database_tables']} total
-Key Tables:{', '.join(info['key_tables'])}
Available Specialized Agents (Auto-Routing):
{chr(10).join(['.'+ agent for agent in info ['available_agents']])}

I automatically route your requests to the right specilaist based in keywords in your question.AgentExecutor
Just ask naturally about customers finance, inventory, or analytics !
      """.strip()
    except Exception as e:
        return f"Error getting system info:{str(e)}"
    
# -------------------------- TOOLS LIST -------------------------
SMART_ROUTER_TOOLS = [
    classify_and_route,
    get_system_info, 
    excute_with_sales_agent, 
    excute_with_finance_agent, 
    excute_with_inventory_agent,
    excute_with_analytics_agent
    ]

#--------------------------- LLM --------------------------------------
llm = get_llm()

#--------------------------- Memory -------------------------------------
'''
def get_memory():
    """Return a conversation buffer memory for the last k messages."""
    return ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
memory = get_memory()
'''
#--------------------------- prompt -------------------------------------
'''def smart_react_prompt():
    """Return the prompt template for the router agent."""
    return ChatPromptTemplate.from_messages([
    ("system", SMART_ROUTER_SYSTEM),
    ("human", "{user_input}")
])'''
prompt = get_react_promp()

#----------------------------- The prompt of the system ------------------------------
SMART_ROUTER_SYSTEM = """ You are the smart router Agent, an intelligent coordinator that automatically. routes request to specialized agents.
The main responsibilities:
1- Automatically classify user requests and route them to the appropriate specialist
2- Excute requests with the right agent and return their results
3- Provide system informatuon when requested
4- Handle general queiries and provide guidance

You habe access to tools that can:
- Automatically classify and route requests to specialiist qgents
- Excute requests with Sales, Finance, Inventory, or Analytics agents
- Provide system information and capabilities

IMPORTANT ROUTING LOGIC:
- For questions about coustomers, orders, leads, sales -> Use excute_with_sales_agent
- For questions about finnances, invoices, payments, money -> Use excute_with_finance_agent
- For questions about prodcuts, stock, inventory, warehouse -> Use excute_with_inventory_agent
- For questions about reports, analytics, insights, trends -> Use excute_with_analytics_agent
- For general system questions -> use get_system_info
- For unclear requests -> use classify_and_route to auto-determine the best agent

Always try to automatically route and excute the request rather than just providing guidance.
"""

#------------------------------ Agent and Executor --------------------------------
agent = create_react_agent(llm =llm, tools=SMART_ROUTER_TOOLS, prompt= prompt)
executor = AgentExecutor(
    agent = agent, 
    tools = SMART_ROUTER_TOOLS,
    verbose = True,
    handle_parsing_errors= True,
    max_iterations=3,
    early_stopping_method="generate")

# --------------------------------- INTERACTIVE RUN -------------------------------
def main_smart_router_agent():
    """ Interactive smart router agent """
    print("Smart Router Agent Ready! I automatically route requests to the right specialist. ")
    print("Examples:")
    print(" 'Show me customers ' -> Auto-routes to Sales Agent")
    print(" 'Financial summary ' -> Auto-routes to Finance Agent")
    print("Check inventory -> Auto-routes to Inventory Agent")
    print(" Sales report -> Auto-routes to Analytics Agent")
    print (" Type 'quit' to exit \n")

    while True:
        user_input = input("Smart Router > ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Exiting Smart Router Agent. Goodbye!")
            break
        try:
            result = executor.invoke({"input": user_input})
            print(f"Smart Router Response: {result['output']}\n")
        except Exception as e:
            print(f"Error while processing request: {str(e)}\n")

# ------------------------------------ MAIN -----------------------------------------
if __name__ == "__main__":
    main_smart_router_agent()





