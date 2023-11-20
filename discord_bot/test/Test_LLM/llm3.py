# Load model directly
import os
os.environ['TRANSFORMERS_CACHE'] = '/nfs/scratch/students/nguyenda81452/itp/CACHE_DIR/huggingface/hub'
os.environ['HF_HOME'] = '/nfs/scratch/students/nguyenda81452/itp/CACHE_DIR/huggingface'

import torch
from dotenv import load_dotenv
from huggingface_hub import login, logout
from ctransformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline

from datetime import datetime

load_dotenv()

hf_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

login(token=hf_token)

prompt = "Was macht ein Bundeskanzler?"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"\n####################### Device: {device} #############################")

model_id = "jphme/em_german_7b_v01"
print(f"\nLLM-Model: {model_id}")

#llm = AutoModelForCausalLM.from_pretrained(model_id, model_file="llama-2-13b-german-assistant-v2.Q4_K_M.gguf", model_type="llama", gpu_layers=50, hf=True)
#print(llm(prompt))
#tokenizer = AutoTokenizer.from_pretrained(llm)

print(f"\n{datetime.now()}  Loading model weights")
generator = pipeline(
    task="text-generation", 
    model=model_id,
    #tokenizer=tokenizer, 
    torch_dtype='auto', #torch.bfloat16, 
    device_map="auto",
    temperature=0.7,
    top_p=0.15,
    top_k=15,
    repetition_penalty=1.1,
    num_return_sequences=1,
    #eos_token_id=tokenizer.eos_token_id,
    max_new_tokens=65,
    #max_length=256,
    )
print(f"\n{datetime.now()}  Starting generating answer:")
answer = generator(prompt, do_sample=True)
print(f"\n{datetime.now()}  {answer[0]['generated_text']}")
print("\n#############################################################################################")
logout()