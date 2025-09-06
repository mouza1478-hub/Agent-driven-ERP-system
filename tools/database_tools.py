import sqlite3
from typing import List, Dict, Optional

DB_PATH = "erp.db"


# ----------------- Sales Agent Tools ----------------------------------------

# ------------------------- Database Connection -------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# Customers
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Orders
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    total REAL,
    status TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")

# Products
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    cost REAL,
    price REAL,
    stock_quantity INTEGER
)
""")

# Leads
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_email TEXT,
    status TEXT,
    score REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert sample data
cursor.execute("INSERT INTO customers (name, email, phone) VALUES ('Alice', 'alice@example.com', '1111111111')")
cursor.execute("INSERT INTO customers (name, email, phone) VALUES ('Bob', 'bob@example.com', '2222222222')")
cursor.execute("INSERT INTO orders (customer_id, total, status) VALUES (1, 100.0, 'completed')")
cursor.execute("INSERT INTO orders (customer_id, total, status) VALUES (2, 200.0, 'pending')")
cursor.execute("INSERT INTO products (name, cost, price, stock_quantity) VALUES ('Product A', 50, 80, 100)")
cursor.execute("INSERT INTO products (name, cost, price, stock_quantity) VALUES ('Product B', 30, 60, 200)")
cursor.execute("INSERT INTO leads (contact_email, status, score) VALUES ('lead1@example.com', 'new', 80)")
cursor.execute("INSERT INTO leads (contact_email, status, score) VALUES ('lead2@example.com', 'contacted', 90)")

conn.commit()
conn.close()
def execute_query(query: str, params: tuple = ()) -> List[Dict[str, any]]:
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


# ------------------------- Analytics Helpers -------------------------
def execute_custom_query(query: str, params: tuple = ()) -> List[Dict]:
    """
    Execute any custom SQL query and return results as a list of dicts.
    Works like a wrapper around execute_query to be used by Analytics Agent.
    """
    return execute_query(query, params)


def get_financial_summary() -> Dict[str, float]:
    """
    Return a basic financial summary calculated from the database:
    - Total revenue (sum of all orders)
    - Total cost (sum of all product costs, if 'cost' column exists)
    - Total profit (revenue - cost)
    """
    try:
        # Total revenue
        revenue_query = "SELECT SUM(total) as total_revenue FROM orders;"
        revenue_res = execute_query(revenue_query)
        total_revenue = revenue_res[0].get('total_revenue', 0) if revenue_res else 0

        # Total cost
        cost_query = "SELECT SUM(cost) as total_cost FROM products;"  # assumes cost column exists
        cost_res = execute_query(cost_query)
        total_cost = cost_res[0].get('total_cost', 0) if cost_res else 0

        # Profit
        total_profit = (total_revenue or 0) - (total_cost or 0)

        return {
            "total_revenue": total_revenue or 0,
            "total_cost": total_cost or 0,
            "total_profit": total_profit
        }
    except Exception as e:
        return {"error": str(e)}
    

def test_database_tools():
    print("\n=== Testing Database Tools ===\n")
    
    # 1️⃣ Check tables in the database
    tables = get_table_names()
    print("Tables in DB:", tables)
    print("-" * 50)

    # 2️⃣ Get first 3 customers
    customers = get_customers()
    print("Sample Customers:", customers[:3])
    print("-" * 50)

    # 3️⃣ Add a test customer
    print("Creating test customer...")
    result = create_customer("Test User", "test@example.com", "1234567890")
    print(result)
    print("-" * 50)

    # 4️⃣ Get orders (first 3)
    orders = get_orders()
    print("Sample Orders:", orders[:3])
    print("-" * 50)

    # 5️⃣ Get leads (first 3)
    leads = get_leads()
    print("Sample Leads:", leads[:3])
    print("-" * 50)

    # 6️⃣ Execute custom query
    query = "SELECT COUNT(*) as total_orders FROM orders;"
    custom_result = execute_query(query)
    print("Custom Query Result:", custom_result)
    print("-" * 50)
''''
if __name__ == "__main__":
    test_database_tools()'''