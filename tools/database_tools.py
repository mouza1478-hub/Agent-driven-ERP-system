import sqlite3
from typing import List, Dict, Optional
from langchain.tools import tool

DB_PATH = "erp.db"

'''
# ----------------- Sales Agent Tools ----------------------------------------

# ------------------------- Core Query Tool -------------------------
@tool
def execute_query(query: str, params: tuple = ()) -> List[Dict]:
    """Execute a SQL query and return results as a list of dicts."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]


# ------------------------- Table Tools -------------------------
@tool
def get_table_names() -> List[str]:
    """Return a list of table names in the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return [f"Error fetching tables: {str(e)}"]


# ------------------------- Customer Tools -------------------------
@tool
def get_customers(
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    customer_id: Optional[int] = None
) -> List[Dict]:
    """Return all customers or filter by name, email, phone, or customer_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM customers WHERE 1=1"
    params = []

    if customer_id:
        query += " AND id = ?"
        params.append(customer_id)
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if email:
        query += " AND email LIKE ?"
        params.append(f"%{email}%")
    if phone:
        query += " AND phone LIKE ?"
        params.append(f"%{phone}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@tool
def create_customer(name: str, email: str, phone: str) -> str:
    """Add a new customer to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone, created_at) VALUES (?, ?, ?, datetime('now'))",
        (name, email, phone)
    )
    conn.commit()
    conn.close()
    return f"Customer '{name}' created successfully."


# ------------------------- Orders Tools -------------------------
@tool
def get_orders(customer_id: Optional[int] = None, order_id: Optional[int] = None) -> List[Dict]:
    """Return all orders, or filter by customer_id or order_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    if customer_id:
        query += " AND customer_id = ?"
        params.append(customer_id)
    if order_id:
        query += " AND id = ?"
        params.append(order_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ------------------------- Leads Tools -------------------------
@tool
def get_leads(
    lead_id: Optional[int] = None,
    contact_email: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict]:
    """Return all leads or filter by lead_id, contact_email, or status."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if lead_id:
        query += " AND id = ?"
        params.append(lead_id)
    if contact_email:
        query += " AND contact_email LIKE ?"
        params.append(f"%{contact_email}%")
    if status:
        query += " AND status = ?"
        params.append(status)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

#---------------------- Clarification --------------------------
@tool
def ask_clarification(question: str) -> str:
    """Prompt the user for clarification."""
    return f"Clarification needed: {question}"

# ------------------------- Financial Summary Tool -------------------------
@tool
def get_financial_summary() -> Dict[str, float]:
    """Return total revenue, total cost, and total profit."""
    try:
        revenue_query = "SELECT SUM(total) as total_revenue FROM orders;"
        revenue_res = execute_query(revenue_query)
        total_revenue = revenue_res[0].get('total_revenue', 0) if revenue_res else 0

        cost_query = "SELECT SUM(cost) as total_cost FROM products;"
        cost_res = execute_query(cost_query)
        total_cost = cost_res[0].get('total_cost', 0) if cost_res else 0

        total_profit = (total_revenue or 0) - (total_cost or 0)

        return {
            "total_revenue": total_revenue or 0,
            "total_cost": total_cost or 0,
            "total_profit": total_profit
        }
    except Exception as e:
        return {"error": str(e)}
'''
# ------------------------- Core Query Tool -------------------------
@tool
def execute_query(query: str, params: tuple = ()) -> List[Dict]:
    """Execute a SQL query and return results as a list of dicts."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]

# ------------------------- Table Tools -------------------------
@tool
def get_table_names() -> List[str]:
    """Return a list of table names in the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return [f"Error fetching tables: {str(e)}"]

# ====================== Customer Tools =========================
@tool
def get_customers(
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    customer_id: Optional[int] = None
) -> List[Dict]:
    """Return all customers or filter by name, email, phone, or customer_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM customers WHERE 1=1"
    params = []

    if customer_id:
        query += " AND id = ?"
        params.append(customer_id)
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if email:
        query += " AND email LIKE ?"
        params.append(f"%{email}%")
    if phone:
        query += " AND phone LIKE ?"
        params.append(f"%{phone}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@tool
def create_customer(name: str, email: str, phone: Optional[str] = None) -> str:
    """Add a new customer to the database. Phone is optional."""
    if not phone:
        phone = "N/A"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone, created_at) VALUES (?, ?, ?, datetime('now'))",
        (name, email, phone)
    )
    conn.commit()
    conn.close()
    return f"Customer '{name}' created successfully."

# ====================== Orders Tools =========================
@tool
def get_orders(customer_id: Optional[int] = None, order_id: Optional[int] = None) -> List[Dict]:
    """Return all orders, or filter by customer_id or order_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    if customer_id:
        query += " AND customer_id = ?"
        params.append(customer_id)
    if order_id:
        query += " AND id = ?"
        params.append(order_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ====================== Leads Tools =========================
@tool
def get_leads(
    lead_id: Optional[int] = None,
    contact_email: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict]:
    """Return all leads or filter by lead_id, contact_email, or status."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if lead_id:
        query += " AND id = ?"
        params.append(lead_id)
    if contact_email:
        query += " AND contact_email LIKE ?"
        params.append(f"%{contact_email}%")
    if status:
        query += " AND status = ?"
        params.append(status)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ====================== Clarification Tool =========================
@tool
def ask_clarification(question: str) -> str:
    """Prompt the user for clarification."""
    return f"Clarification needed: {question}"

# ====================== Financial Summary Tool =========================
@tool
def get_financial_summary() -> Dict[str, float]:
    """Return total revenue, total cost, and total profit."""
    try:
        revenue_query = "SELECT SUM(total) as total_revenue FROM orders;"
        revenue_res = execute_query(revenue_query)
        total_revenue = revenue_res[0].get('total_revenue', 0) if revenue_res else 0

        cost_query = "SELECT SUM(cost) as total_cost FROM products;"
        cost_res = execute_query(cost_query)
        total_cost = cost_res[0].get('total_cost', 0) if cost_res else 0

        total_profit = (total_revenue or 0) - (total_cost or 0)

        return {
            "total_revenue": total_revenue or 0,
            "total_cost": total_cost or 0,
            "total_profit": total_profit
        }
    except Exception as e:
        return {"error": str(e)}

# ------------------------- Analytics Helpers -------------------------
@tool
def execute_custom_query(query: str, params: tuple = ()) -> List[Dict]:
    """
    Execute any custom SQL query and return results as a list of dictionaries.
    """
    return execute_query(query, params)


@tool
def get_financial_summary() -> Dict[str, float]:
    """
    Returns a basic financial summary:
    - total revenue
    - total cost
    - total profit
    """
    try:
        revenue_query = "SELECT SUM(total) as total_revenue FROM orders;"
        revenue_res = execute_query(revenue_query)
        total_revenue = revenue_res[0].get('total_revenue', 0) if revenue_res else 0

        cost_query = "SELECT SUM(cost) as total_cost FROM products;"
        cost_res = execute_query(cost_query)
        total_cost = cost_res[0].get('total_cost', 0) if cost_res else 0

        total_profit = (total_revenue or 0) - (total_cost or 0)

        return {
            "total_revenue": total_revenue or 0,
            "total_cost": total_cost or 0,
            "total_profit": total_profit
        }
    except Exception as e:
        return {"error": str(e)}

