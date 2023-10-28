import sqlite3
import pandas as pd
import torch
from transformers import BertModel, BertTokenizer
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from scrap.db_init import db_get_df, db_save_df
import argparse

def get_model():
    model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def proccessSentence(token_ids, model, tokenizer):
    if len(token_ids) == 0:
        # Handle the case when the token list is empty, for example, return a default embedding or raise an exception.
        # For demonstration purposes, we'll return a zero tensor as the default embedding.
        return torch.zeros(768)

    token_ids = [101] + token_ids + [102]

    attention_mask = [1 if token_id != 0 else 0  for token_id in token_ids]
    token_ids_tensor = torch.tensor([token_ids], dtype=torch.int64)
    attetion_mask_tensor = torch.tensor([attention_mask], dtype=torch.int64)

    with torch.no_grad():
        outputs = model(token_ids_tensor, attetion_mask_tensor)
        hidden_states = outputs[2]

    # stack the layer list 
    token_embeddings = torch.stack(hidden_states, dim=0)
    # remove the batches dim
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # Swap dimensions 0 and 1.
    token_embeddings = token_embeddings.permute(1,0,2)
    # average all token embeds
    layer_vecs = torch.mean(token_embeddings, dim=0)


    # last layer
    embed_1 = layer_vecs[12]

    # Calculate the average of layer 3 to 13
    embed_2 = torch.mean(layer_vecs[2:], dim=0)

    # sum of layer 3 to 13
    embed_3 = layer_vecs[2:].sum(0)

    # sum of last four layer
    embed_4 = layer_vecs[-4:].sum(0) 

    #concat last four layers
    embed_5 = torch.cat([layer_vecs[i] for i in [-1,-2,-3,-4]], dim=0)
    
    print(embed_1[3], token_ids[3])
    return embed_1, embed_2, embed_3, embed_4, embed_5


def create_and_save_embeddings(chunk_count, chunk_id):
    model, tokenizer = get_model()
    df = db_get_df("chunk_embeddings", ["filename", "chunk_text", "chunk_id", "chunk_tokens_json"])

    workers = chunk_count
    chunk_size = len(df) // workers
    offset = chunk_count * chunk_id
    my_chunk = df.iloc[offset:offset+chunk_size].copy()  # Create a copy to avoid SettingWithCopyWarning

    embed_matrix = [proccessSentence(json.loads(tokens), model, tokenizer) for tokens in tqdm(my_chunk["chunk_tokens_json"])]

    for i in range(5):
        col_name = f"chunk_word_embeddings_{i+1}"
        my_chunk[col_name] = [json.dumps(word_embedding[i].tolist()) for word_embedding in embed_matrix]

        print(f"got {col_name}")

    # db_save_df(my_chunk, f'chunk_word_embeddings_{chunk_id}')


def main():
    
    parser = argparse.ArgumentParser(description="Your script description")
    parser.add_argument("--chunk_count", type=int, required=True, help="How many chunks the data is splitted - how many proccesses will run")
    parser.add_argument("--chunk_id", type=int, required=True, help="which chunk this proccess will calculate")

    args = parser.parse_args()

    create_and_save_embeddings(args.chunk_count, args.chunk_id)


if __name__ == "__main__":
    main()
