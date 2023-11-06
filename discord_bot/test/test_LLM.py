import os
from dotenv import load_dotenv
import torch
from huggingface_hub import login, logout

load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

login(token=hf_token)
# logout()

# Use a pipeline as a high-level helper
from transformers import pipeline, TextGenerationPipeline

generator: TextGenerationPipeline = pipeline(
    "text-generation", model="meta-llama/Llama-2-7b-chat-hf"
)
print()
print(generator)

answer = generator("Wer ist der schnellste Man der Welt?", return_text=True)

print(answer)
print(answer["generated_text"])

logout()
