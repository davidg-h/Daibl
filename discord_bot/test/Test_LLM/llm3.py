# Load model directly
import os
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

llm = AutoModelForCausalLM.from_pretrained("TheBloke/llama-2-13B-German-Assistant-v2-GGUF", model_file="llama-2-13b-german-assistant-v2.Q2_K.gguf", hf=True, gpu_layers=100).to(device)
tokenizer = AutoTokenizer.from_pretrained(llm)

generator = pipeline(
    task="text-generation", 
    model=llm, 
    tokenizer=tokenizer, 
    torch_dtype=torch.float16, 
    device_map="auto",
    temperature=0.8,
    top_p=0.15,
    top_k=10,
    repetition_penalty=1.1,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_new_tokens=80,
    do_sample=True,
    #max_length=256
    )
print(generator(prompt)[0]['generated_text'])

logout()