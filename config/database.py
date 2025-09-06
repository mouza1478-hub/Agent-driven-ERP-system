import sqlite3
from typing import List, Dict, Any

DB_PATH = "erp.db"

def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a SQL query and return results as a list of dicts."""
    try:
        conn = get_connection()
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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return [f"Error fetching tables: {str(e)}"]
    
 # Testing the connection
try:
    conn = get_connection()
    print(" Connection OK")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

# Test 2: Tables
tables = get_table_names()
print("Tables:", tables)

# Test 3: Execute a simple query
if "customers" in tables:
    result = execute_query("SELECT * FROM customers LIMIT 3;")
    print("Sample Customers:", result)
else:
    print("No 'customers' table found")