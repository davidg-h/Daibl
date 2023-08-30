
from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states = True)

def question_embeddings(message):

    tokens = tokenizer.tokenize(message)
    segments_ids = [1] * len(tokens)
    token_idss = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([token_idss])
    segments_tensors = torch.tensor([segments_ids])
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]
    
    token_vecs = hidden_states[-2][0]
    # Calculate the average of all 22 token vectors.
    question_embedding = torch.mean(token_vecs, dim=0)
    print ("Our final sentence embedding vector of shape:", question_embedding)

    df = load_embeddings()
    df["distance"] = [cos_distance(question_embedding, file_embedding) for file_embedding in df["word_embeddings"]]
    
    [print(text) for text in df.sort_values(by="distance")["text"].head(5)]

def load_embeddings():
    database = 'discord_bot/scrap/html.sqlite'
    sql = """
    SELECT filename, title, text
    FROM html_attrs
    """

    con = sqlite3.connect(database)
    df = pd.read_sql_query(sql, con)
    con.close()
    return df


def cos_distance(vec1, vec2):
    return torch.cosine_similarity(vec1, vec2)
    

question_embeddings("Wer ist Gallwitz?")
#only 5 best documents 


