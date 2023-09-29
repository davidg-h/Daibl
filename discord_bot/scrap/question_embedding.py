
from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from db_init import initialize_database
from spacy_keywordextraction import extraction
import json

DATABASE_PATH = "discord_bot/scrap/html.sqlite"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states = True)

def question_embeddings(message):

    tokens = tokenizer.tokenize(message)
    segments_ids = [0 if token == "[PAD]" else 1 for token in tokens]
    token_idss = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([token_idss])
    segments_tensors = torch.tensor([segments_ids])
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]
    
    token_vecs = hidden_states[-2][0]
    # Calculate the average of all 22 token vectors.
    sentence_embedding = torch.mean(token_vecs, dim=0)
    # print ("Our final sentence embedding vector of shape:", sentence_embedding)
    return sentence_embedding
    

def calculate_document_question_distance(sentence_embedding,document_embedding):
    
    # Calculate the cosine similarity between question and document
    diff_bank = 1 - cosine(sentence_embedding, document_embedding)

    # print('Vector similarity for *different* meanings:  %.2f' % diff_bank)
    return diff_bank

def get_5_most_similar_documents(message):
    # Initialisiere den DataFrame mit der Funktion aus db_init.py
    df = initialize_database(DATABASE_PATH)
    question_embedding=question_embeddings(message)
    df["distance"]=[calculate_document_question_distance(question_embedding,json.loads(document_embedding))for document_embedding in df["word_embeddings"]]
    most_similar_documents = df.nsmallest(5, "distance")

    return most_similar_documents["text"]