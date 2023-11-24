import os
os.environ['TRANSFORMERS_CACHE'] = 'D:\.cache\huggingface\hub'
os.environ['HF_HOME'] = 'D:\.cache\huggingface'

import torch
from huggingface_hub import login
from ctransformers import AutoModelForCausalLM, AutoTokenizer # loading of Quantized LLM
from transformers import pipeline # loading of hf LLMs


class ModelCommunicator:
    """ 
    Handels communication with large language models 

    ...

    Attributes
    ----------
    hf_api_token : str
        huggingface api token
    """

    def __init__(self, hf_api_token):
        
        #setup
        login(token=hf_api_token)
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model_id = "jphme/em_german_7b_v01"
        quantized_file = "" # only set if loading quantized model (model.gguf)
        self.model = None
        
        # load the model
        if quantized_file != "":
            llm = AutoModelForCausalLM.from_pretrained(model_id, model_file=quantized_file, model_type="llama", gpu_layers=50, hf=True).to(device)
            tokenizer = AutoTokenizer.from_pretrained(llm)
            self.model = pipeline(
                task="text-generation", 
                model=llm,
                tokenizer=tokenizer, 
                torch_dtype=torch.bfloat16, 
                device_map='auto',
                temperature=0.7,
                top_p=0.15,
                top_k=15,
                repetition_penalty=1.1,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id,
                max_new_tokens=65,
                #max_length=256,
            )
        else:
            self.model = pipeline(
                task="text-generation", 
                model=model_id,
                torch_dtype=torch.bfloat16, 
                device_map='auto',
                temperature=0.7,
                top_p=0.15,
                top_k=15,
                repetition_penalty=1.1,
                num_return_sequences=1,
                max_new_tokens=65,
                #max_length=256,
            )

    def returnPromptText(self, question):
        """ process and return answer of LLM """
        
        answer = self.model(question, do_sample=True)
        return answer[0]['generated_text']
