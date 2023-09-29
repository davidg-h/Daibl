import sqlite3
import pandas as pd

database_path = "discord_bot/scrap/html.sqlite"


def db_get_df(tablename, coloumns):
    con = sqlite3.connect(database_path)
    html_df = pd.read_sql_query(f"SELECT {', '.join(coloumns)} FROM {tablename}", con)
    con.close()
    return html_df

def db_save_df(df, tablename):
    with sqlite3.connect(database_path) as con:
        df.to_sql(tablename, con, index=False, if_exists='replace')