from sqlalchemy import create_engine, Engine
from dotenv import load_dotenv
import os

load_dotenv()
POSTGRES_CONN=os.environ.get("POSTGRES_CONN")

def database_connection() -> Engine:
    if POSTGRES_CONN is None:
        raise ValueError("POSTGRES_CONN is empty")
    try:
        postgres_db=create_engine(POSTGRES_CONN)
        with postgres_db.connect():
            print("Connection succeded")

        return postgres_db
    except Exception as e:
        raise Exception(f"Error occurred while connection to database: {e}")
    
if __name__=="__main__":
    try:
        db_engine = database_connection()
    except Exception as e:
        print(f"Critical error: {e}")