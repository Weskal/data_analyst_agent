import pyodbc
from config.settings import ConfigManager
from data.db_schema import get_schema
from agent.llm_setup import return_client

# Constants

configManager = ConfigManager()
conn_str = configManager.conn_str
schema = get_schema(conn_str)
openai_client = return_client()

def gen_sql_query(question, client, schema):
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""Você é um especialista em SQL Server. Gere APENAS a query SQL, sem explicações.

        {schema}

                Regras:
                - Retorne APENAS o código SQL
                - Use apenas SELECT
                - Use nomes exatos das tabelas e colunas do schema
                """
                            },
                            {
                                "role": "user",
                                "content": question
                            }
                        ],
                        temperature=0.1
                    )
                    
    content = response.choices[0].message.content
    query = content.strip()
    if query.startswith("```"):
        query = query.split("\n", 1)[1]
        query = query.rsplit("```", 1)[0]

    return query

def validate_select_only():
    # Validate if the query is a real select
    pass
def run_sql_query():
    pass

def main():
    
    question = "Query para retornar a quantidade de funcionários total da tabela funcionários"
    
    sql_query = gen_sql_query(question, openai_client, schema)

if __name__ == '__main__':
    main()