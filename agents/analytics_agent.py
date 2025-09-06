#------------------------------ Analytics Agent ------------------------------

import os 
import sys
from pathlib import Path 

#Working with file and directory paths in a platform-independent manner
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.output_parsers import StructuredOutputParser
from config.llm import get_llm
from config.prompts import get_react_prompt
from config.database import execute_query



# --------------------- Tools for Analytics Agent ---------------------
from config.database import execute_query
from langchain.tools import tool
from datetime import datetime, timedelta

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
        avg_order_value = execute_query(avg_order_query)

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

        # Assemble result
        result = {
            "top_customers": top_customers,
            "sales_by_status": sales_by_status,
            "monthly_sales_last_6_months": monthly_sales,
            "average_order_value": avg_order_value[0]['avg_order_value'] if avg_order_value else 0,
            "new_customers_last_6_months": new_customers
        }

        return result

    except Exception as e:
        return {"error": str(e)}


# ----------------- Customer Analytics -----------------
@tool
def get_customer_analytics(_: str) -> dict:
    """
    Returns customer-related metrics including:
    - Customer growth
    - Customer activity (orders placed)
    - Lead status
    """
    try:
        # Customer growth
        customer_growth_query = """
        SELECT strftime('%Y-%m', created_at) AS month,
               COUNT(*) AS new_customers
        FROM customers
        GROUP BY month
        ORDER BY month ASC;
        """
        customer_growth = execute_query(customer_growth_query)

        # Customer activity
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

        # Lead status
        lead_status_query = """
        SELECT status, COUNT(*) AS count
        FROM leads
        GROUP BY status;
        """
        lead_status = execute_query(lead_status_query)

        return {
            "customer_growth": customer_growth,
            "customer_activity": customer_activity,
            "lead_status": lead_status
        }

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

        return {
            "top_products_by_sales": top_products,
            "top_products_by_reviews": top_reviewed,
            "inventory_summary": inventory
        }

    except Exception as e:
        return {"error": str(e)}


# ----------------- Aggregated Analytics Tools -----------------
Analytics_tools = [
    get_sale_analytics,
    get_customer_analytics,
    get_product_analytics
]