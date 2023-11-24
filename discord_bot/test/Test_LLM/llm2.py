# Use a pipeline as a high-level helper
from transformers import pipeline, AutoTokenizer
import os
from dotenv import load_dotenv
from huggingface_hub import login, logout
import torch

load_dotenv()

hf_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

login(token=hf_token)

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)

llama_pipeline = pipeline(
    "text-generation",  # LLM task
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

def get_llama_response(prompt: str) -> None:
    """
    Generate a response from the Llama model.

    Parameters:
        prompt (str): The user's input/question for the model.

    Returns:
        None: Prints the model's response.
    """
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    print("Chatbot:", sequences[0]['generated_text'])

prompt = 'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n'
get_llama_response(prompt)

logout()