from langchain.agents import initialize_agent, AgentType
from langchain import ChatOpenAI
from config.settings import ConfigManager
from data.db_schema import get_schema
from llm_setup import return_client
from langchain.tools.base import BaseTool
import tools

class DataAnalystAgent():
    def __init__(self) -> None:
        
        configManager = ConfigManager()
        conn_str = configManager.conn_str
        schema = get_schema(conn_str)
        openai_client = return_client()
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key =configManager.openai_api_key
        )
        self.conn_str = conn_str
        self.schema = schema
        self.openai_client = openai_client
        
        self.tools = [v for v in vars(tools).values() if isinstance(v, BaseTool)]
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
    def ask(self, question):
        """Receives user question and orients the agent which tool should use"""
        
        #self.agent.
    
    def display_result(self, result):
        pass
        
def main():
    
    analyst_agent = DataAnalystAgent()
    
    question = "Qual o total de funcionários da tabela de funcionários?"
    
    result = analyst_agent.ask(question)
    
    analyst_agent.display_result(result)
    
if __name__ == '__main__':
    main()