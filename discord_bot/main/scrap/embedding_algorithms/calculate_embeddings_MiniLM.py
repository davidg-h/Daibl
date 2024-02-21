from db_init import db_get_df, db_save_df
import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def calculate_MiniLM():
    df=db_get_df("html_attr_combined")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    def get_and_serialize_embeddings(text):
        embeddings = model.encode([text])[0]
        return json.dumps(embeddings.tolist())

    tqdm.pandas(desc="Calculating Embeddings")
    df['embeddings'] = df['text'].progress_apply(get_and_serialize_embeddings)
    db_save_df(df,"MiniLM_embeddings")

