#------------------------------ Analytics Agent ------------------------------

import os 
import sys
from pathlib import Path 
import sqlite3
from typing import List, Dict


#Working with file and directory paths in a platform-independent manner
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.agents import create_react_agent, AgentExecutor
from tools.database_tools import execute_custom_query, get_financial_summary
from langchain.tools import tool
from langchain.output_parsers import StructuredOutputParser
from config.llm import get_llm
from config.prompts import get_analytics_prompt
from config.database import execute_query
from datetime import datetime, timedelta



# --------------------- Tools for Analytics Agent ---------------------

# ----------------- Sales Analytics -----------------

# --------------------- Tools for Analytics Agent ---------------------

# ----------------- Sales Analytics -----------------
@tool
def get_sale_analytics(_: str) -> dict:
    """
    Returns comprehensive sales metrics including:
    - Top customers
    - Sales by status
    - Monthly sales (last 6 months)
    - Average order value
    - New customers in last 6 months
    """
    try:
        # Top 10 customers by total order value
        top_customers_query = """
        SELECT c.name AS customer_name,
               COUNT(o.id) AS order_count,
               SUM(o.total) AS total_value
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id, c.name
        ORDER BY total_value DESC
        LIMIT 10;
        """
        top_customers = execute_query(top_customers_query)

        # Sales by status
        sales_by_status_query = """
        SELECT status,
               COUNT(*) AS order_count,
               SUM(total) AS total_value
        FROM orders
        GROUP BY status;
        """
        sales_by_status = execute_query(sales_by_status_query)

        # Monthly sales for last 6 months
        six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-01")
        monthly_sales_query = f"""
        SELECT strftime('%Y-%m', created_at) AS month,
               COUNT(*) AS order_count,
               SUM(total) AS total_value
        FROM orders
        WHERE created_at >= '{six_months_ago}'
        GROUP BY month
        ORDER BY month ASC;
        """
        monthly_sales = execute_query(monthly_sales_query)

        # Average order value
        avg_order_query = "SELECT AVG(total) AS avg_order_value FROM orders;"
        avg_order_value_result = execute_query(avg_order_query)
        avg_order_value = avg_order_value_result[0]['avg_order_value'] if avg_order_value_result else 0

        # New customers in last 6 months
        new_customers_query = f"""
        SELECT strftime('%Y-%m', created_at) AS month,
               COUNT(*) AS new_customers
        FROM customers
        WHERE created_at >= '{six_months_ago}'
        GROUP BY month
        ORDER BY month ASC;
        """
        new_customers = execute_query(new_customers_query)

        # Final structured result
        analytics = {
            "top_customers": top_customers,
            "sales_by_status": sales_by_status,
            "monthly_sales_last_6_months": monthly_sales,
            "average_order_value": avg_order_value,
            "new_customers_last_6_months": new_customers
        }

        # Formatted report
        report = f"""
SALES ANALYTICS REPORT
========================
TOP 10 CUSTOMERS:
{chr(10).join([f"- {c['customer_name']}: {c['order_count']} orders, ${c['total_value']:.2f}" for c in top_customers])}

SALES BY STATUS:
{chr(10).join([f"- {c['status']}: {c['order_count']} orders, ${c['total_value']:.2f}" for c in sales_by_status])}

MONTHLY SALES (LAST 6 MONTHS):
{chr(10).join([f"- {c['month']}: {c['order_count']} orders, ${c['total_value']:.2f}" for c in monthly_sales])}

AVERAGE ORDER VALUE: ${analytics['average_order_value']:.2f}

NEW CUSTOMERS (LAST 6 MONTHS):
{chr(10).join([f"- {c['month']}: {c['new_customers']} new customers" for c in new_customers])}
""".strip()

        return {"analytics": analytics, "report": report}

    except Exception as e:
        return {"error": str(e)}

# ----------------- Product Analytics -----------------
@tool
def get_product_analytics(_: str) -> dict:
    """
    Returns product-related metrics including:
    - Top 10 products by sales
    - Top 10 products by reviews
    - Inventory summary
    """
    try:
        # Top products by sales
        top_products_query = """
        SELECT p.name AS product_name,
               SUM(oi.quantity) AS total_sold,
               SUM(oi.price * oi.quantity) AS total_revenue
        FROM products p
        JOIN order_items oi ON p.id = oi.product_id
        GROUP BY p.id, p.name
        ORDER BY total_sold DESC
        LIMIT 10;
        """
        top_products = execute_query(top_products_query)

        # Top products by reviews
        top_reviewed_query = """
        SELECT p.name AS product_name,
               COUNT(r.id) AS review_count,
               AVG(r.rating) AS avg_rating
        FROM products p
        LEFT JOIN reviews r ON p.id = r.product_id
        GROUP BY p.id, p.name
        ORDER BY avg_rating DESC
        LIMIT 10;
        """
        top_reviewed = execute_query(top_reviewed_query)

        # Inventory summary
        inventory_query = """
        SELECT name AS product_name, stock_quantity
        FROM products
        ORDER BY stock_quantity ASC;
        """
        inventory = execute_query(inventory_query)

        # Formatted report
        report = f"""
PRODUCT ANALYTICS REPORT
========================
TOP 10 PRODUCTS BY SALES:
{chr(10).join([f"- {p['product_name']}: {p['total_sold']} sold, ${p['total_revenue']:.2f}" for p in top_products])}

TOP 10 PRODUCTS BY REVIEWS:
{chr(10).join([f"- {p['product_name']}: {p['review_count']} reviews, avg rating {p['avg_rating']:.2f}" for p in top_reviewed])}

INVENTORY SUMMARY (Lowest to Highest Stock):
{chr(10).join([f"- {p['product_name']}: {p['stock_quantity']} units" for p in inventory])}
""".strip()

        return {
            "top_products_by_sales": top_products,
            "top_products_by_reviews": top_reviewed,
            "inventory_summary": inventory,
            "report": report
        }

    except Exception as e:
        return {"error": str(e)}
# --------------------------------- Customer Analytics Tool ------------------------
@tool
def get_customer_analytics(_: str) -> dict:
    """
    Returns customer-related metrics including:
    - Customer growth per month
    - Customer activity (orders placed, total spent)
    - Lead status and average score
    """
    try:
        # Customer growth per month
        customer_growth_query = """
        SELECT strftime('%Y-%m', created_at) AS month,
               COUNT(*) AS new_customers
        FROM customers
        GROUP BY month
        ORDER BY month ASC;
        """
        customer_growth = execute_query(customer_growth_query)

        # Customer activity (orders and spending)
        customer_activity_query = """
        SELECT c.name AS customer_name,
               COUNT(o.id) AS order_count,
               SUM(o.total) AS total_spent
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id, c.name
        ORDER BY total_spent DESC;
        """
        customer_activity = execute_query(customer_activity_query)

        # Lead status and average score
        lead_status_query = """
        SELECT status,
               COUNT(*) AS count,
               AVG(CASE WHEN score IS NOT NULL THEN score ELSE 0 END) AS avg_score
        FROM leads
        GROUP BY status;
        """
        lead_status = execute_query(lead_status_query)

        # Build a readable analytics report
        report = f"""
CUSTOMER ANALYTICS REPORT
========================
CUSTOMER GROWTH PER MONTH:
{chr(10).join([f"- {c['month']}: {c['new_customers']} new customers" for c in customer_growth])}

CUSTOMER ACTIVITY:
{chr(10).join([f"- {c['customer_name']}: {c['order_count']} orders, ${c['total_spent']:.2f} spent" for c in customer_activity])}

LEAD STATUS:
{chr(10).join([f"- {c['status']}: {c['count']} leads, avg score {c['avg_score']:.2f}" for c in lead_status])}
""".strip()

        return {
            "customer_growth": customer_growth,
            "customer_activity": customer_activity,
            "lead_status": lead_status,
            "report": report
        }

    except Exception as e:
        return {"error": str(e)}
@tool
def run_custom_query(input: str) -> List[Dict]:
    """Run any SQL query (read-only recommended) and return the results."""
    return execute_custom_query(input)

@tool
def get_financial_summary_tool(_: str) -> Dict[str, float]:
    """
    Return a basic financial summary:
    - total revenue
    - total cost
    - total profit
    """

    query = """
    SELECT 
        SUM(oi.unit_price * oi.quantity) AS total_revenue,
        SUM(oi.cost * oi.quantity) AS total_cost,
        SUM(oi.unit_price * oi.quantity) - SUM(oi.cost * oi.quantity) AS total_profit
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    WHERE o.status = 'completed'
    """

    try:
        conn = sqlite3.connect("erp.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "total_revenue": result["total_revenue"] or 0.0,
                "total_cost": result["total_cost"] or 0.0,
                "total_profit": result["total_profit"] or 0.0
            }
        else:
            return {"total_revenue": 0.0, "total_cost": 0.0, "total_profit": 0.0}
    except Exception as e:
        return {"error": str(e)}
# ----------------- Aggregated Analytics Tools -----------------
Analytics_tools = [
    get_sale_analytics,
    get_customer_analytics,
    run_custom_query,
    get_product_analytics, 
    get_financial_summary_tool
]

# ----------------------------- LLM -----------------------------
llm = get_llm()

# ----------------------------- Parser --------------------------
output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=[
        {
            "name": "Action",
            "description": "The tool to call (must be one of the analytics tools)"
        },
        {
            "name": "Action Input",
            "description": "JSON input to the tool. If no input is needed, use {}"
        }
    ]
)

# ----------------------- Building the Analytics Agent -----------------
prompt = get_analytics_prompt()
agent = create_react_agent(
    llm=llm,
    tools=Analytics_tools,
    prompt=prompt
)

executor = AgentExecutor(
    agent=agent,
    tools=Analytics_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iteration=3,
    early_stopping_method="generate"
)

def main_analytics_agent():
    """
    Interactive Analytics Agent
    This agent handles all analytics requests and provides comprehensive reports.
    """
    print("\n=== Analytics Agent Ready! ===")
    print("I can provide insights on sales, customers, and products.")
    print("Examples of commands:")
    print(" - 'Sales report'           -> Sales analytics")
    print(" - 'Customer report'        -> Customer analytics")
    print(" - 'Product report'         -> Product analytics")
    print("Type 'quit', 'exit', or 'q' to exit.\n")

    while True:
        user_input = input("Analytics Agent > ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Exiting Analytics Agent. Goodbye!")
            break
        try:
            result = executor.invoke({"user_input": user_input})
            print(f"Analytics Agent Response:\n{result['output']}\n")
        except KeyboardInterrupt:
            print("Analytics Agent shutting down")
        except Exception as e:
            print(f"Error: {e}")

# ------------------------------------ MAIN -----------------------------------------
if __name__ == "__main__":
    main_analytics_agent()