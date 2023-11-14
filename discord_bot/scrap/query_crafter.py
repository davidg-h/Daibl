from transformers import BertModel, BertTokenizer
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from scrap.question_embedding import get_5_most_similar_documents
from scrap.db_init import db_get_df
from scrap.spacy_keywordextraction import extraction
import json


# best 5 documents as context
def get_query_embeddings(message):
    best_documents = get_5_most_similar_documents(message)
    query="\n----Dokument----\n".join(best_documents)+"\n"+"in regard of the documents above,anwser the following question: \n"+ message.replace("$daibl ", "")
    print(query)
    return query

# scrapy keywordextraction
# has to be caped of
# TODO: tf idf
def get_query_extraction(message):
    dokuments = extraction(message)
    dokuments_text = "\n----Dokument----\n".join(dokuments)
    query=dokuments_text[:1200] + "\n"+"in regard of the documents above, anwser the following question: \n"+ message.replace("$daibl ", "")
    print(query)
    return query

# all documents as context
# throws error on api
def get_query_all(message):
    df = db_get_df("word_embeddings", ["text"])
    documents = df["text"]
    query="\n----Dokument----\n".join(documents)+"\n"+"in regard of the documents above,anwser the following question: \n"+ message.replace("$daibl ", "")
    print(query)
    return query