# 🧠 NLQ to SQL

An AI-powered Natural Language Query (NLQ) to SQL application that allows users to interact with a database using natural language.

Instead of writing SQL queries manually, users can ask questions in plain English, and the system converts those questions into SQL queries and retrieves the corresponding results from the database.

## 🚀 Features

- Convert natural language questions into SQL queries
- Connect with a relational database
- Use an LLM for SQL query generation
- Execute generated SQL queries
- Return database results to the user
- Environment variable support using `.env`

## 🏗️ Project Structure

```text
NLQ TO SQL/
│
├── app.py
├── database.py
├── llm_engine.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```
```text
⚠️ .env is excluded from GitHub using .gitignore and should never contain publicly exposed API keys.
```

## ⚙️ Technologies Used

-Python
-SQL
-Large Language Model (LLM)
-Natural Language Processing
-Database Connectivity
-FastAPI / Streamlit (update according to your implementation)

## 🔄 Workflow

```text
User Question
      ↓
Natural Language Input
      ↓
LLM / SQL Generation
      ↓
Generated SQL Query
      ↓
Database
      ↓
Query Execution
      ↓
Result
```

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the project directory
```bash
cd NLQ-TO-SQL
```

### 3. Create a virtual environment
```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:
```bash
venv\Scripts\activate
```
### 5. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a .env file in the project root directory.

Example:
```env
OPENAI_API_KEY=your_api_key_here
```
Do not upload your actual API key to GitHub.

## ▶️ Running the Application

```bash
python main.py
```
Update the command above according to the application's entry point.

## 👨‍💻 Author

**Sandeep Bisht**

MCA | Artificial Intelligence & Machine Learning

📧 **Email:** [ssandeepbisht2402@gmail.com](mailto:ssandeepbisht2402@gmail.com)