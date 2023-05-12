from llm_rs import Llama

class ModelCommunicator:
    
    def __init__(self, model_path):
        #load the model 
        self.model = Llama(model_path)

    def returnPromptText(self, question):
        #generate response
        return self.model.generate(question).text