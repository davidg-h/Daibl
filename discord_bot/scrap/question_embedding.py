
from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from scrap.db_init import db_get_df
from scrap.spacy_keywordextraction import extraction
import json

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states = True)

def question_embeddings(message):
    message = "[CLS]" + message + "[SEP]"
    tokens = tokenizer.tokenize(message)
    attetion_mask = [0 if token == "[PAD]" else 1 for token in tokens]
    token_idss = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([token_idss])
    attetion_mask_tensor = torch.tensor([attetion_mask])

    with torch.no_grad():
        outputs = model(tokens_tensor, attetion_mask_tensor)
        hidden_states = outputs[2]
    

    # initial embeddings can be taken from 0th layer of hidden states
    word_embed_2 = hidden_states[0]

    # sum of all hidden states
    word_embed_3 = torch.stack(hidden_states).sum(0)

    # sum of second to last layer
    word_embed_4 = torch.stack(hidden_states[2:]).sum(0) 

    # sum of last four layer
    word_embed_5 = torch.stack(hidden_states[-4:]).sum(0) 

    #concat last four layers
    word_embed_6 = torch.cat([hidden_states[i] for i in [-1,-2,-3,-4]], dim=-1)

    
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
    df = db_get_df("word_embeddings", ["word_embeddings", "text"])
    question_embedding = question_embeddings(message)
    df["distance"] = [calculate_document_question_distance(question_embedding,json.loads(document_embedding))for document_embedding in df["word_embeddings"]]
    most_similar_documents = df.nsmallest(5, "distance")
    print(f"question embedding: {question_embedding}")
    print(most_similar_documents["distance"])

    return most_similar_documents["text"]