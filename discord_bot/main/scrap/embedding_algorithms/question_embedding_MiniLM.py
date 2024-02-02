from scrap.db_init import db_get_df, db_save_df
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


def get_most_similar_articles(query,top_n):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings_df=db_get_df("embeddings_paraphrase_MiniLM_L6_v2")
    # Convert back to lists.
    embeddings_df["text_embedding"] = [json.loads(text_embedding_json) for text_embedding_json in embeddings_df["text_embedding_json"]]
    query_embedding = model.encode(query, show_progress_bar=True)
    similarities = []

    for index, row in tqdm(embeddings_df.iterrows(), total=len(embeddings_df), desc="Calculating similarities"):
        
        similarity = cosine_similarity([query_embedding], [row["text_embedding"]])[0][0]

        similarities.append({'filename': row['filename'],
                            'title': row['title'],
                            'text': row['text'], 
                            'similarity': similarity})

    similarities_df = pd.DataFrame(similarities)
    most_similar_articles = similarities_df.nlargest(top_n, 'similarity')['text']

    return most_similar_articles



