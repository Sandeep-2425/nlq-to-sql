import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import streamlit as st
load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "nlq_to_sql"),
}

_BLOCKED_KEYWORDS = ("DROP", "TRUNCATE", "GRANT", "REVOKE")

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

def get_schema() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]

    schema_lines = []
    for table in tables:
        cursor.execute(f"DESCRIBE {table};")
        columns = cursor.fetchall()
        col_desc = ", ".join(f"{col[0]} {col[1]}" for col in columns)
        schema_lines.append(f"Table {table}: {col_desc}")

    cursor.close()
    conn.close()
    return "\n".join(schema_lines)

def run_query(sql_query: str):
    upper_sql = sql_query.upper()

    if any(keyword in upper_sql for keyword in _BLOCKED_KEYWORDS):
        return None, "Blocked: generated query contains a disallowed keyword."

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        if cursor.description:
            results = cursor.fetchall()
            columns = []
            for desc in cursor.description:
                columns.append(desc[0])
            cursor.close()
            conn.close()
            return columns, results
        else:
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            return None, f"Query executed successfully. {affected_rows} row(s) affected."
    except Error as err:
        return None, str(err)