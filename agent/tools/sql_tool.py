import pyodbc as db
import pandas as pd
from typing import Any
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
                "content": f"""Você é um especialista em SQL Server.

                SCHEMA DISPONÍVEL:
                {schema}

                1. Gere APENAS a query SQL, sem explicações
                2. Use apenas tabelas/colunas do schema acima
                3. Queries devem ser somente SELECT (read-only)
                4. Use aliases claros e JOINs explícitos
                """
                            },
                            {
                                "role": "user",
                                "content": question
                            }
                        ],
                        temperature=0
                    )
                    
    content = response.choices[0].message.content
    query = content.strip()
    if query.startswith("```"):
        query = query.split("\n", 1)[1]
        query = query.rsplit("```", 1)[0]

    return query

def danger_query(query):
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'EXEC']
    if any(keyword in query.upper() for keyword in dangerous_keywords):
        return True
    
def run_sql_query(query: str, conn_str) -> dict:
    """Executes SQL Query"""
    
    if danger_query(query):
        return {"error": "modifying operations not allowed", "message":"failure"}
    
    try:
        conn: Any = db.connect(conn_str, readonly=True)
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            
            return {
                "dataframe": df,
                "markdown": df.to_markdown(index=False),
                "json": df.to_dict(orient='records'),
                "rows": len(df),
                "columns": list(df.columns),
                "message": "success"
            }
        
        else: 
            return {"warning": "no records found for the query: {query}", "message":"sucess"}
   
    except Exception as e:
        return {"error": {e}, "message":"failure"}

def interpret_results(question, query, result, generate_graph=False):
    """AI interprets the result in natural language"""
    
    # Pedir para a IA explicar o resultado na hora da interpretação
    # passar 0 = O pedido
    # passar 1 = A query
    # passar 2 = O resultado
    # gerar = Gráfico + explicação ?

def main():
    
    question = "Qual o total de funcionários na tabela de funcionários?"
    
    # Criar uma função para ler a questão e verificar se o usuário pediu algum gráfico/tabela ou visual do resultado se pediu, utilizar a tool apropriada para gerar e
    # depois devolver como True of False
    #generate_graph = False
    
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            sql_query = gen_sql_query(question, openai_client, schema)
            
        except db.Error as e:
            if attempt < max_retries - 1:
                print("Trying one more time to execute the query")
                sql_query = gen_sql_query(question, openai_client, schema)
            else:
                return {"error": f"Failure after {max_retries} tries: {str(e)}"}
        
    result_dict = run_sql_query(sql_query, conn_str)
    
    if result_dict.get('message') == 'success':
        print("\n" + "="*50)
        print("Query Results")
        print("="*50 + "\n")
        print(result_dict['markdown'])
        print(f"\nRows: {result_dict['rows']}")
        print(f"Columns: {', '.join(result_dict['columns'])}\n")
    else:
        print(f"Error: {result_dict.get('error')}")
        
    #final_response = interpret_results(question, sql_query, result_dict, generate_graph)

if __name__ == '__main__':
    main()