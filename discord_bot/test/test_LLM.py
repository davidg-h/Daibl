import os
from dotenv import load_dotenv
from langchain import HuggingFaceHub, PromptTemplate, LLMChain

load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

s = "Who is Usain Bolt?"

llm = HuggingFaceHub(
    repo_id="bigscience/bloom", 
    #model_kwargs={"temperature":1e-10},
    huggingfacehub_api_token=hf_token
)

template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(s))
