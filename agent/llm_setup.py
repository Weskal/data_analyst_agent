from openai import OpenAI
from config.settings import ConfigManager

def return_client():
    configManager = ConfigManager()
    openai_api_key = configManager.openai_api_key
    client = OpenAI(api_key=openai_api_key)
    
    return client