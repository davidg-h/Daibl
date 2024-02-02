import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv # TODO 

load_dotenv()
database_path = os.getenv("DATABASE_PATH")

def db_get_df(tablename="chunk_embeddings", coloumns=["*"]):
    if type(coloumns) is not list:
        raise Exception("needs a list as argument for coloumns parameter")
    con = sqlite3.connect(database_path)
    html_df = pd.read_sql_query(f"SELECT {', '.join(coloumns)} FROM {tablename}", con)
    con.close()
    return html_df

def db_save_df(df, tablename):
    with sqlite3.connect(database_path) as con:
        df.to_sql(tablename, con, index=False, if_exists='replace')
