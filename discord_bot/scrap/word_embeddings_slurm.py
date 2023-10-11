import sqlite3
import pandas as pd
import torch
from transformers import BertModel, BertTokenizer
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from scrap.db_init import db_get_df
import argparse

DATABASE = '/home/neumannvi84434/Daibl/daibl/discord_bot/scrap/html.sqlite'


def get_model():
    model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def proccessSentence(tokens, model, tokenizer):
    if len(tokens) == 0:
        # Handle the case when the token list is empty, for example, return a default embedding or raise an exception.
        # For demonstration purposes, we'll return a zero tensor as the default embedding.
        return torch.zeros(768)

    tokens = ["CLS"] + tokens + ["SEP"]

    attention_mask = [1 if token != "[PAD]" else 0  for token in tokens]
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_ids_tensor = torch.tensor([token_ids], dtype=torch.int64)
    attetion_mask_tensor = torch.tensor([attention_mask], dtype=torch.int64)

    with torch.no_grad():
        outputs = model(token_ids_tensor, attetion_mask_tensor)
        hiddenDocuments_states = outputs[2]

    tokenDocuments_vecs = hiddenDocuments_states[-2][0]
    sentenceDocument_embedding = torch.mean(tokenDocuments_vecs, dim=0)

    # # initial embeddings can be taken from 0th layer of hidden states
    # word_embed_2 = hidden_states[0]

    # # sum of all hidden states
    # word_embed_3 = torch.stack(hidden_states).sum(0)

    # # sum of second to last layer
    # word_embed_4 = torch.stack(hidden_states[2:]).sum(0) 

    # # sum of last four layer
    # word_embed_5 = torch.stack(hidden_states[-4:]).sum(0) 

    # #concat last four layers
    # word_embed_6 = torch.cat([hidden_states[i] for i in [-1,-2,-3,-4]], dim=-1)
    

    return sentenceDocument_embedding


def create_and_save_embeddings_chunk(chunk_df, model, tokenizer):
    word_embeddings = [proccessSentence(json.loads(tokens), model, tokenizer) for tokens in tqdm(chunk_df["chunk_tokens_json"])]
    chunk_df["chunk_word_embeddings"] = [json.dumps(word_embedding.tolist()) for word_embedding in word_embeddings]
    return chunk_df


def create_and_save_embeddings(chunk_count, chunk_id):
    model, tokenizer = get_model()
    df = db_get_df("chunk_word_embeddings", ["filename", "chunk_text", "chunk_id", "chunk_tokens_json"])

    workers = chunk_count
    chunk_size = len(df) // workers
    offset = chunk_count * chunk_id
    my_chunk = df[offset:offset+chunk_size] 

    word_embeddings = [proccessSentence(json.loads(tokens), model, tokenizer) for tokens in tqdm(my_chunk["chunk_tokens_json"])]
    my_chunk["chunk_word_embeddings"] = [json.dumps(word_embedding.tolist()) for word_embedding in word_embeddings]
    print("got embeddings")

    with sqlite3.connect(DATABASE) as con:
        df.to_sql(f'chunk_word_embeddings_{chunk_id}', con, index=False, if_exists='replace')

def main():
    
    parser = argparse.ArgumentParser(description="Your script description")
    parser.add_argument("--chunk_count", type=int, required=True, help="How many chunks the data is splitted - how many proccesses will run")
    parser.add_argument("--chunk_id", type=int, required=True, help="which chunk this proccess will calculate")

    args = parser.parse_args()

    
    create_and_save_embeddings(args.chunk_count, args.chunk_id)


if __name__ == "__main__":
    main()
