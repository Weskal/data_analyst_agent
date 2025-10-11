from langchain.agents import initialize_agent, AgentType
from langchain import ChatOpenAI
from langchain.tools import Tool
from sql_tool import run_sql_query, gen_sql_query
from python_tool import run_python_code
from visualization_tool import generate_plot
from interpretation import interpret_results

tools = [
    Tool.from_function(func=gen_sql_query, name="SQLGenerator", description="Generates SQL Queries based on NLP"),
    Tool.from_function(func=run_sql_query, name="SQLExecutor", description="Executes SQL Functions"),
    Tool.from_function(func=interpret_results, name="ResultInterpeter", description="Interprets results from question + query + output"),
    Tool.from_function(func=run_python_code, name="PythonExecutor", description="Executes Python Code"),
    Tool.from_function(func=generate_plot, name="GraphCreator", description="Generates visualization")
]