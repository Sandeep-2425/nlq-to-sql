import streamlit as st
from database import get_schema, run_query
from llm_engine import convert_nlq_to_sql

st.title("NLQ to SQL")
st.write("Ask a question about the company database in plain English.")

if "question" not in st.session_state:
    st.session_state.question = ""
if "history" not in st.session_state:
    st.session_state.history = [] 

def clear_question():
    st.session_state.question = ""
    
user_question = st.text_input(
    "Your question:",
    key="question"
)

col1, col2 = st.columns([1, 1])
with col1:
    run_clicked = st.button("Run Query", type="primary")
with col2:
    st.button(
        "Clear",
        on_click=clear_question)

if run_clicked:
    if user_question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        schema = get_schema()

        with st.spinner("Generating SQL..."):
            try:
                sql_query = convert_nlq_to_sql(user_question, schema)
            except Exception as e:
                st.error(f"LLM Error: {e}")
                st.stop()

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        columns, results = run_query(sql_query)

        st.subheader("Results")
        if columns is not None:
            if results:
                st.table([dict(zip(columns, row)) for row in results])
            else:
                st.info("Query ran successfully but returned no rows.")
        else:
            if results.startswith("Query executed successfully"):
                st.success(results)
            else:
                st.error(f"Execution Error: {results}")

        st.session_state.history.append({
            "question": user_question,
            "sql": sql_query,
            "columns": columns,
            "results": results,
        })

if st.session_state.history:
    st.divider()
    st.subheader("Query History")

    for entry in reversed(st.session_state.history):
        with st.expander(entry["question"]):
            st.code(entry["sql"], language="sql")
            if entry["columns"] is not None and entry["results"]:
                st.table([dict(zip(entry["columns"], row)) 
                          for row in entry["results"]])
            elif entry["columns"] is not None:
                st.info("No rows returned.")
            else:
                if entry["results"].startswith("Query executed successfully"):
                    st.success(entry["results"])
                else:
                    st.error(f"Error: {entry['results']}")