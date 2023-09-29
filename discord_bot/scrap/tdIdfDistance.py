import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

DATABASE_PATH = "discord_bot/scrap/html.sqlite"
def initialize_database(database_path):
    con = sqlite3.connect(database_path)
    html_df = pd.read_sql_query("SELECT filename,title,text,tokens,term_frequency FROM tf_idf", con)
    con.close()
    return html_df

df=initialize_database(DATABASE_PATH)


frage_text = "welche studiengänge gibt es?"

# Berechne die TF-IDF-Werte der Frage
vectorizer = TfidfVectorizer()
frage_tfidf = vectorizer.fit_transform([frage_text])

# Berechne die Ähnlichkeit zwischen Frage und Dokumenten
cosine_similarities = linear_kernel(frage_tfidf, df.drop(['filename', 'title', 'text', 'tokens'], axis=1))

# Jetzt sind cosine_similarities[i] die Kosinusähnlichkeiten zwischen der Frage und Dokument i.

# Hier verwenden wir tqdm, um den Fortschritt anzuzeigen
for i in tqdm(range(len(cosine_similarities)), desc="Berechne Ähnlichkeiten", unit=" Dokument"):
    # cosine_similarities[i] enthält die Ähnlichkeit zwischen Frage und Dokument i
    ähnlichkeit = cosine_similarities[i]

# Index des Dokuments mit der höchsten Ähnlichkeit
best_document_index = cosine_similarities.argmax()

# Der Name des besten Dokuments
best_document_name = df.iloc[best_document_index]['filename']

print(f'Das beste Dokument ist: {best_document_name}')
