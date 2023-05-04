import subprocess

class ModelCommunicator:

    def returnPromptText(self,MODEL,CHAT, question):
        result = subprocess.run([CHAT, '-m', MODEL, '-p', question], stdout=subprocess.PIPE, shell=True)
        resultText=result.stdout.decode()
        return resultText