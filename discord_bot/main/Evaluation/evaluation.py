import sys
sys.path.append('..')
sys.path.append('../..')
from scrap.query_crafter import construct_prompt
from scrap.embedding_algorithms.tdIdfDistance import get_most_similar_articles_tf_idf
from scrap.embedding_algorithms.question_embedding_MiniLM import get_most_similar_articles_MiniLM
from LLM.ServerCommunicator import server_get_answer
from dotenv import load_dotenv
load_dotenv()
import os
import torch
from huggingface_hub import login
from transformers import pipeline # loading of hf LLMs
import gc
import pandas as pd
import asyncio

os.environ['TRANSFORMERS_CACHE'] = '/nfs/scratch/students/nguyenda81452/CACHE_DIR'
os.environ['HF_HOME'] = '/nfs/scratch/students/nguyenda81452/CACHE_DIR'

def get_most_similar_articles_for_specified_embediing_model(embedding_model,question,document_amount):
    
    embeddings_model_dict = {
        'MiniLM': get_most_similar_articles_MiniLM,
        'TF-IDF': get_most_similar_articles_tf_idf
    }
     
    get_most_similar_articles = embeddings_model_dict.get(embedding_model)
    result = get_most_similar_articles(question,document_amount)
    
    return result

def return_prompt_anwser(model, query_prompt):
    """ process and return answer of LLM """
    
    answer = model(query_prompt, do_sample=True)
    return answer[0]['generated_text']

async def get_anwser_from_model(model_id, query_prompt,model):
    answer=""
    if model_id == 'vicuna_70b':
        answer = server_get_answer(query_prompt)
    elif model_id == 'lmsys/vicuna-13b-v1.5': 
        answer = return_prompt_anwser(model,query_prompt)
    elif model_id  == 'meta-llama/Llama-2-13b-chat-hf':
        answer = return_prompt_anwser(model,query_prompt)

    return answer
async def generate_response(model_id,document_amount,embedding_model,question,model):
    anwser=""
    documents = get_most_similar_articles_for_specified_embediing_model(embedding_model,question,document_amount)
    query_prompt = construct_prompt(documents, question) 
    anwser = await get_anwser_from_model(model_id,query_prompt,model)
    
    return anwser


def model_load(model_id):
  HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
  login(token=HUGGINGFACEHUB_API_TOKEN)
  device = "cuda:0" if torch.cuda.is_available() else "cpu"

  model = pipeline(
    task="text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map='auto',
    temperature=0.3,
    top_p=0.15,
    top_k=15,
    repetition_penalty=1.1,
    num_return_sequences=1,
    max_new_tokens=128,
    #max_length=256,
  )
  return model

def model_unload(model):

    del model
    gc.collect()
    torch.cuda.empty_cache()

async def evaluate():
    # Erstellen Sie eine leere DataFrame
    columns = ["Model", "Document Amount", "Embeddings Model", "Question", "Response"]
    df = pd.DataFrame(columns=columns)

    # Ihre Daten
    ##"vicuna_70b"
    model_ids = ["lmsys/vicuna-13b-v1.5","meta-llama/Llama-2-13b-chat-hf"]
    document_amounts = [1, 5, 10]
    embeddings_models=["MiniLM","TF-IDF"]
    questions=["Wie ist die Email Adresse von Professor Gallwitz?",
            "Was soll ich beachten, wenn ich eine Prüfung anmelden will?",
            "Welche voraussetzungen, muss ich für den Master Studiengang erfüllen?",
            "Welche Professoren gibt es an der Fakultät Soziale Arbeit?",
            "Wann und was muss ich im IT-Projekt machen?"]

    data = []
    model= None
    for model_id in model_ids:
        if(model_id != "vicuna_70b"):
            model= model_load(model_id)
        for document_amount in document_amounts:
            for embeddings_model in embeddings_models:
                for question in questions:
                    response = await generate_response(model_id, document_amount, embeddings_model, question,model)
                    print("response:",response)
                    data.append([model_id, document_amount, embeddings_model, question, response])
        model_unload(model)
            
    df = pd.concat([df, pd.DataFrame(data, columns=columns)], ignore_index=True)

    # Speichern Sie die DataFrame in eine Excel-Datei
    df.to_excel('output.xlsx', index=False)



async def main():
    await evaluate()

# Starte den asynchronen Kontext
if __name__ == "__main__":
    asyncio.run(main())
