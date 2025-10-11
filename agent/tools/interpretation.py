from agent.llm_setup import return_client
from typing import Dict, Any

def interpret_results(question, query, result, generate_graph=False):
    """AI interprets the result in natural language"""
    
    # Pedir para a IA explicar o resultado na hora da interpretação
    # passar 0 = O pedido
    # passar 1 = A query
    # passar 2 = O resultado
    # gerar = Gráfico + explicação ?