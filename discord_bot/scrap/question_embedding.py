
from transformers import BertModel, BertTokenizer
import torch
from scipy.spatial.distance import cosine
from scrap.db_init import initialize_database
import json
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
    sentence_embedding = torch.mean(token_vecs, dim=0)
    print ("Our final sentence embedding vector of shape:", sentence_embedding)
    return sentence_embedding
    

def calculate_document_question_distance(sentence_embedding,document_embedding):
    
    # Calculate the cosine similarity between question and document
    diff_bank = 1 - cosine(sentence_embedding, document_embedding)
    print('Vector similarity for *different* meanings:  %.2f' % diff_bank)
    return diff_bank

def get_5_most_similar_documents(message):
    database_path = "discord_bot\scrap\html.sqlite"
    # Initialisiere den DataFrame mit der Funktion aus db_init.py
    df = initialize_database(database_path)
    question_embedding=question_embeddings(message)
    df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding)) for document_embedding in df["word_embeddings"]]
    sorted_df = df.sort_values(by="distance", ascending=True)
    most_similar_documents = sorted_df.head(5)
    return most_similar_documents["text"]

print(get_5_most_similar_documents("wer ist gallwitz"))


