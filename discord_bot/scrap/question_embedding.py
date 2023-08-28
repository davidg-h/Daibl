
from transformers import BertModel, BertTokenizer
import torch

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

    
#only 5 best documents 


