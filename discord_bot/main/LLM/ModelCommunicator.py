from langchain.llms import HuggingFaceHub

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


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
        # load the model
        self.model = HuggingFaceHub(
            repo_id="bigscience/mt0-base",
            model_kwargs={"temperature": 1e-10},
            huggingfacehub_api_token=hf_api_token
        )

    def returnPromptText(self, question):
        """ process and return answer of LLM """

        self.template = """Question: {question}

        Answer: """
        self.prompt = PromptTemplate(
            template=self.template, input_variables=["question"])

        llm_chain = LLMChain(prompt=self.prompt, llm=self.model)
        return llm_chain.run(question)
