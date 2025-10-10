import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

class ConfigManager():
    
    def __init__(self):

        load_dotenv('.env')

        openai_api_key = os.getenv("OPENAI_API_KEY")
        conn_str = os.getenv('CONN_STR')
        sql_db = os.getenv('SQL_DB')

        self.openai_api_key = openai_api_key
        self.conn_str = conn_str
        self.sql_db = sql_db
        
    # def create_dir  
     
    def validateConfig(self):
        errors = []
        
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY not configured in .env file.")
        
        if not self.conn_str:
            errors.append("CONN_STR not configured in .env file.")
            
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(errors))