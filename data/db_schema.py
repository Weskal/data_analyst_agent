import pyodbc
from config.settings import ConfigManager

configManager = ConfigManager()

def get_schema(conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    database = configManager.sql_db
    
    cursor.execute(f"USE {database}")

    query = """
    SELECT 
        TABLE_SCHEMA,
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE
    FROM 
        INFORMATION_SCHEMA.COLUMNS
    WHERE 
        TABLE_SCHEMA = 'dbo'
    ORDER BY 
        TABLE_NAME, ORDINAL_POSITION
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    schema_dict = {}
    for row in results:
        schema_name, table_name, col_name, data_type = row
        
        full_table_name = f"{schema_name}.{table_name}"
        
        if full_table_name not in schema_dict:
            schema_dict[full_table_name] = []
        
        col_info = f"  - {col_name} ({data_type}"
            
        schema_dict[full_table_name].append(col_info)

    schema_txt = ""
    for table, columns in schema_dict.items():
        schema_txt += f"\nTabela: {table}\n"
        schema_txt += "\n".join(columns)
        schema_txt += "\n"
    
    return schema_txt