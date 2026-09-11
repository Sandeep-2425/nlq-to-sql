from datetime import date, datetime
from decimal import Decimal

from database import get_schema, run_query
from llm_engine import convert_nlq_to_sql


def _format_value(value):
    """Convert DB types into clean display strings."""
    if isinstance(value, Decimal):
        return f"{value:.2f}"
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if value is None:
        return "NULL"
    return str(value)


def _format_row(row):
    return " | ".join(_format_value(v) for v in row)


def ask_database(user_question):
    print(f"\n==========================================")
    print(f"User Question: '{user_question}'")

    schema = get_schema()

    try:
        sql_query = convert_nlq_to_sql(user_question, schema)
    except Exception as e:
        print(f"LLM Error: {e}")
        return

    print(f"Generated SQL: {sql_query}")

    columns, results = run_query(sql_query)

    if columns is not None:
        print("\nQuery Results:")
        if columns:
            print(" | ".join(columns))
            print("-" * 40)
        for row in results:
            print(_format_row(row))
    else:
        print(f"Execution Error: {results}")


if __name__ == "__main__":
    ask_database("List all employees earning more than 60000")
    ask_database("Count the total number of employees in Engineering")
    ask_database("List all employees along with their department manager")
    ask_database("List all employees along with their department manager")
    ask_database("Show employees who work in a department managed by Bob Jones")