import sqlite3
from typing import List, Dict, Optional

DB_PATH = "erp.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# ----------------- Sales Agent Tools ----------------------------------------

def get_customers(
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    customer_id: Optional[int] = None
) -> List[Dict]:
    """Return all customers or filter by name, email, phone, or customer_id."""
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone, created_at) VALUES (?, ?, ?, datetime('now'))",
        (name, email, phone)
    )
    conn.commit()
    conn.close()
    return f"✅ Customer '{name}' created successfully."


def get_orders(customer_id: Optional[int] = None, order_id: Optional[int] = None) -> List[Dict]:
    """Return all orders, or filter by customer_id or order_id."""
    conn = get_connection()
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
    conn = get_connection()
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


