#from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
#from scrap.question_embedding import get_5_most_similar_documents
from scrap.db_init import db_get_df
#from scrap.spacy_keywordextraction import extraction
import json
from scrap.embedding_algorithms.question_embedding_MiniLM import get_most_similar_articles
from scrap.embedding_algorithms.msmarco_roberta_base_v3 import get_most_similar_articles_msmarco


# best 5 documents as context
# def get_query_embeddings(message):
#     best_documents = get_5_most_similar_documents(message)
#     query="\n----Dokument----\n".join(best_documents)+"\n"+"in regard of the documents above,anwser the following question: \n"+ message.replace("$daibl ", "")
#     print(query)
#     return query

# scrapy keywordextraction
# has to be caped of
# TODO: tf idf
# def get_query_extraction(message):
#     dokuments = extraction(message)
#     dokuments_text = "\n----Dokument----\n".join(dokuments)
#     query=dokuments_text[:1200] + "\n"+"in regard of the documents above, anwser the following question: \n"+ message.replace("$daibl ", "")
#     print(query)
#     return query

def construct_query(documents, message):
    query=f"""
        {'----document----'.join(documents)}
        \n----document----\n
        in regard of the documents above, anwser the following question: \n
        {message.replace('$daibl ', '')}
        """

    print(query)
    return query
    

# all documents as context
# throws error on api
def get_query_all(message):
    df = db_get_df("word_embeddings", ["text"])
    documents = df["text"]
    query = construct_query(documents, message)
    return query

# get 5 best articles with MiniLM-L6-v2
def get_query_embeddings_MiniLM(message):
    documents = get_most_similar_articles(message,5)
    query = construct_query(documents, message)   
    return query

# get 5 best articles with embeddings_msmarco_distilroberta_base_v3
def get_query_embeddings_Msmarco(message):
    documents = get_most_similar_articles_msmarco(message,5)
    query = construct_query(documents, message) 
    return query