from scrap.db_init import db_get_df
from scrap.embedding_algorithms.question_embedding_MiniLM import (
    get_most_similar_articles_MiniLM,
)
from scrap.embedding_algorithms.msmarco_roberta_base_v3 import (
    get_most_similar_articles_msmarco,
)
from scrap.embedding_algorithms.tdIdfDistance import get_most_similar_articles_tf_idf
import re


# could be made much more readable and debuggable with llama-index
def construct_prompt(documents, message):
    prompt = f"""
        {'----document----'.join(documents)}
        \n----document----\n"""
    prompt = re.sub(r"\s+", " ", prompt)  ## truncates multiple whitespace to one space
    prompt = prompt[:7000]
    prompt = (
        prompt
        + f"""
        Mithilfe der oben stehenden Dokumente beantworte die folgende Frage: \n
        {message.replace('$daibl ', '')}
        """
    )

    print(prompt)
    return prompt


# all documents as context
# throws error on api because all documents are too much context
# or the context has to be cut at a certain point leaving the model with complet unrelated context
def get_query_all(message):
    df = db_get_df("word_embeddings", ["text"])
    documents = df["text"]
    prompt = construct_prompt(documents, message)
    return prompt


# get 5 best articles with MiniLM-L6-v2
def get_query_embeddings_MiniLM(message, document_amount):
    documents = get_most_similar_articles_MiniLM(message, document_amount)
    prompt = construct_prompt(documents, message)
    return prompt


# get 5 best articles with embeddings_msmarco_distilroberta_base_v3
def get_query_embeddings_Msmarco(message):
    documents = get_most_similar_articles_msmarco(message, 5)
    prompt = construct_prompt(documents, message)
    return prompt


def get_query_TF_IDF(message, document_amount):
    documents = get_most_similar_articles_tf_idf(message, document_amount)
    prompt = construct_prompt(documents, message)
    return prompt
