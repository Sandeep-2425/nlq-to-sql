import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL = os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b")

MAX_RETRIES = 3
RETRY_DELAY = 2 


PROMPT_TEMPLATE = """You are an expert MySQL assistant.

Given the database schema below, translate the user's natural language request into a valid MySQL query.

### Database Schema:
{schema}

### Rules:
- Return ONLY the raw SQL query.
- Do NOT wrap the query in markdown.
- Do NOT add explanations.
- Generate the appropriate SQL command based on the user's request.
- Allowed SQL commands:
  * SELECT
  * INSERT
  * UPDATE
  * DELETE
  * CREATE
  * ALTER
- Never generate:
  * DROP
  * TRUNCATE
  * GRANT
  * REVOKE
- Use valid MySQL syntax.
- Do NOT convert INSERT, UPDATE, DELETE, CREATE, or ALTER into SELECT statements.
- If the request cannot be fulfilled with the allowed SQL commands, return:
  INVALID_REQUEST

### User Request:
{question}

### SQL Query:
"""


def _call_groq(prompt: str) -> str:
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def _clean_sql(raw_text: str) -> str:
    text = raw_text.strip()
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1)
    return text.strip().rstrip(";").strip()


def convert_nlq_to_sql(user_question: str, schema_text: str) -> str:
    prompt = PROMPT_TEMPLATE.format(schema=schema_text, question=user_question)

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = _call_groq(prompt)
            sql = _clean_sql(raw)
            if not sql:
                raise ValueError("Model returned empty SQL.")
            return sql
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)

    raise RuntimeError(f"Failed to get SQL from Groq after {MAX_RETRIES} attempts: {last_error}")