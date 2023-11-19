# Load model directly
import os
os.environ['TRANSFORMERS_CACHE'] = 'D:\.cache\huggingface\hub'
os.environ['HF_HOME'] = 'D:\.cache\huggingface'

import torch
from dotenv import load_dotenv
from huggingface_hub import login, logout
from ctransformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline


load_dotenv()

hf_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

login(token=hf_token)

prompt = "Wer war Napoleon?"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_id = "jphme/Llama-2-13b-chat-german"

#llm = AutoModelForCausalLM.from_pretrained(model_id, model_file="llama-2-13b-german-assistant-v2.Q4_K_M.gguf", model_type="llama", gpu_layers=50, hf=True)
#print(llm(prompt))
#tokenizer = AutoTokenizer.from_pretrained(llm)

generator = pipeline(
    task="text-generation", 
    model=model_id,
    #tokenizer=tokenizer, 
    torch_dtype=torch.float16, 
    device_map="auto",
    temperature=0.8,
    top_p=0.15,
    top_k=10,
    repetition_penalty=1.1,
    num_return_sequences=1,
    #eos_token_id=tokenizer.eos_token_id,
    max_new_tokens=50,
    do_sample=True,
    #max_length=256,
    )
answer = generator(prompt)
print(answer[0]['generated_text'])

logout()