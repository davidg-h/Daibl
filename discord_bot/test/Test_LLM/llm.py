import os
from dotenv import load_dotenv
from huggingface_hub import login, logout
from sympy import false
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

load_dotenv()

hf_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

login(token=hf_token)

prompt = "Wer war Napoleon?"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_id = r"C:\Users\David\Desktop\llama_model\itp\llama2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_id)
#model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

generator = pipeline(
    task="text-generation", 
    model=model_id, 
    tokenizer=tokenizer, 
    torch_dtype=torch.float16, 
    device_map="auto",
    temperature=0.1,
    top_p=0.15,
    top_k=10,
    repetition_penalty=1.1,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    #max_new_tokens=50,
    max_length=100)
print(generator(prompt)[0]['generated_text'])


""" encoding = tokenizer(prompt, padding=True, return_tensors='pt').to(device)

with torch.no_grad():
    outputs = model.generate(**encoding)
gen_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Output:\n" + 100 * '-')
print(gen_text) """

logout()