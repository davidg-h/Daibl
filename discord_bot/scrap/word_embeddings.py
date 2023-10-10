import sqlite3
import pandas as pd
import torch
from transformers import BertModel, BertTokenizer
import json
from tqdm import tqdm

DATABASE = '/home/neumannvi84434/Daibl/daibl/discord_bot/scrap/html.sqlite'


def get_df():
	
	sql = """
	SELECT filename, title, text, tokens
	FROM word_embeddings
	"""

	con = sqlite3.connect(DATABASE)
	df = pd.read_sql_query(sql, con)
	con.close()
	return df

def get_model():
	model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
	return (model, tokenizer)

def proccessSentence(tokens):
    if len(tokens) == 0:
        # Handle the case when the token list is empty, for example, return a default embedding or raise an exception.
        # For demonstration purposes, we'll return a zero tensor as the default embedding.
        return torch.zeros(768)

    # Ensure the token sequence length is no longer than the maximum sequence length the model can handle (512)
    if len(tokens) > 512:
        tokens = tokens[:512]

    # Padding the token sequence to the maximum sequence length if it's shorter
    if len(tokens) < 512:
        tokens += ['[PAD]'] * (512 - len(tokens))

    attention_mask = [1 if token != "[PAD]" else 0  for token in tokens]
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_ids_tensor = torch.tensor([token_ids], dtype=torch.int64)
    attetion_mask_tensor = torch.tensor([attention_mask], dtype=torch.int64)

    with torch.no_grad():
        outputs = model(token_ids_tensor, attetion_mask_tensor)
        hiddenDocuments_states = outputs[2]

    tokenDocuments_vecs = hiddenDocuments_states[-2][0]
    sentenceDocument_embedding = torch.mean(tokenDocuments_vecs, dim=0)
    
    print( json.dumps(sentenceDocument_embedding.numpy().tolist()))

    return sentenceDocument_embedding.numpy().tolist()


model, tokenizer = get_model()

df = get_df()
print(df["tokens"][3])
word_embeddings = [proccessSentence(json.loads(tokens)) for tokens in tqdm(df["tokens"])]
df["word_embeddings"] = [json.dumps(word_embedding) for word_embedding in word_embeddings]
print("got embeddings")



with sqlite3.connect(DATABASE) as con:
    df.to_sql('word_embeddings', con, index=False, if_exists='replace')