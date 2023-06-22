from langchain import HuggingFaceHub, PromptTemplate, LLMChain


class ModelCommunicator:
    def __init__(self, hf_api_token):
        # load the model
        self.model = HuggingFaceHub(
            repo_id="bigscience/bloom",
            model_kwargs={"temperature":1e-10},
            huggingfacehub_api_token=hf_api_token
        )
        
        self.template = """Question: {question}
        
        Answer: """
        self.prompt = PromptTemplate(template=self.template, input_variables=["question"])

    def returnPromptText(self, question):
        
        llm_chain = LLMChain(prompt=self.prompt, llm=self.model)
        return llm_chain.run(question)
