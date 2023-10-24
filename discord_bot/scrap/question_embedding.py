
from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from scrap.db_init import db_get_df
# from scrap.spacy_keywordextraction import extraction
import json

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states = True)

def question_embeddings(message):

    if len(message) == 0:
        # Handle the case when the token list is empty, for example, return a default embedding or raise an exception.
        # For demonstration purposes, we'll return a zero tensor as the default embedding.
        return torch.zeros(768)
    
    message = "[CLS]" + message + "[SEP]"
    tokens = tokenizer.tokenize(message)
    attention_mask = [1 if token != "[PAD]" else 0  for token in tokens]
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_ids_tensor = torch.tensor([token_ids], dtype=torch.int64)
    attention_mask_tensor = torch.tensor([attention_mask], dtype=torch.int64)



    with torch.no_grad():
        outputs = model(token_ids_tensor, attention_mask_tensor)
        hidden_states = outputs[2]

    # stack the layer list 
    token_embeddings = torch.stack(hidden_states, dim=0)
    # remove the batches dim
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # Swap dimensions 0 and 1.
    token_embeddings = token_embeddings.permute(1,0,2)
    # average all token embeds
    layer_vecs = torch.mean(token_embeddings, dim=0)


    # # last layer
    # embed_1 = layer_vecs[12]

    # Calculate the average of layer 3 to 13
    embed_2 = torch.mean(layer_vecs[2:], dim=0)

    # # sum of layer 3 to 13
    # embed_3 = layer_vecs[2:].sum(0)

    # # sum of last four layer
    # embed_4 = layer_vecs[-4:].sum(0) 

    # #concat last four layers
    # embed_5 = torch.cat([layer_vecs[i] for i in [-1,-2,-3,-4]], dim=0)
    

    return embed_2
    

def calculate_document_question_distance(sentence_embedding,document_embedding):
    
    # Calculate the cosine similarity between question and document
    diff_bank = 1 - cosine(sentence_embedding, document_embedding)

    # print('Vector similarity for *different* meanings:  %.2f' % diff_bank)
    return diff_bank

def get_5_most_similar_documents(message):
    # Initialisiere den DataFrame mit der Funktion aus db_init.py
    df = db_get_df("chunk_embeddings", ["chunk_word_embeddings_2", "chunk_text"])
    question_embedding = question_embeddings(message)
    df["distance"] = [calculate_document_question_distance(question_embedding,json.loads(document_embedding))for document_embedding in df["chunk_word_embeddings_2"]]
    most_similar_documents = df.nsmallest(4, "distance")
    print(f"question embedding: {question_embedding}")
    print(most_similar_documents["distance"])

    return most_similar_documents["chunk_text"]