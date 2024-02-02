from scrap.db_init import db_get_df, db_save_df
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_most_similar_articles_tf_idf(message,document_amount):
    df = db_get_df("chunk_embeddings")

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['chunk_text'])
    question_tfidf = tfidf_vectorizer.transform([message])
    similarities = cosine_similarity(question_tfidf, tfidf_matrix)
    similarity_df = pd.DataFrame({
        'similarity': similarities[0],
        'text': df['chunk_text']
    })
    sorted_similarity_df = similarity_df.sort_values(by='similarity', ascending=False)

    # Print the top N most relevant documents (e.g., top 5)
    relevant_documents = sorted_similarity_df.head(document_amount)
    return relevant_documents["text"]
