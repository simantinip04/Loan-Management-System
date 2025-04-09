import pyodbc
from util.db_property_util import read_db_properties

def get_db_connection(properties_file='db.properties'):
    props = read_db_properties(properties_file)
    
    conn_str = (
        f"DRIVER={props['driver']};"
        f"SERVER={props['server']};"
        f"DATABASE={props['database']};"
        f"Trusted_Connection=yes;"
    )

    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except Exception as e:
        print("Database connection failed:", e)
        return None