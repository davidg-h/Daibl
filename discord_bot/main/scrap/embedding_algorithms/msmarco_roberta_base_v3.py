from scrap.db_init import db_get_df, db_save_df
import json
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

def get_most_similar_articles_msmarco(query, top_n):
    model = SentenceTransformer('msmarco-distilbert-base-v4')
    embeddings_df = db_get_df("embeddings_msmarco_distilroberta_base_v3")
    embeddings_df["text_embedding"] = [json.loads(text_embedding_json) for text_embedding_json in embeddings_df["text_embedding_json"]]

    query_embedding = model.encode(query, show_progress_bar=True)
    similarities = []

    for index, row in tqdm(embeddings_df.iterrows(), total=len(embeddings_df), desc="Calculating similarities"):
        passage_embedding = row["text_embedding"]
        similarity = util.cos_sim(query_embedding, passage_embedding)
        
        similarities.append({'filename': row['filename'],
                            'title': row['title'],
                            'text': row['text'], 
                            'similarity': similarity})

    similarities_df = pd.DataFrame(similarities)
    # Entferne Zeilen mit NaN (leeren Zellen)
    similarities_df = similarities_df.dropna(subset=['similarity'])

    # Konvertiere 'similarity' in 'float'
    similarities_df['similarity'] = similarities_df['similarity'].astype(float)
    most_similar_articles = similarities_df.nlargest(top_n, 'similarity')['text']

    return most_similar_articles

# query = 'How big is London'
# most_similar = get_most_similar_articles_msmarco(query, 5)
# print(most_similar)
