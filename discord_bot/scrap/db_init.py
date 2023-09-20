import sqlite3
import pandas as pd

def initialize_database(database_path):
    con = sqlite3.connect(database_path)
    html_df = pd.read_sql_query("SELECT filename, title, text ,word_embeddings FROM word_embeddings", con)
    con.close()
    return html_df
