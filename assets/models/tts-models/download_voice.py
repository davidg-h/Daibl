import os
from getpass import getpass
from huggingface_hub import hf_hub_download, login, logout

login(token=getpass("\nEnter your hugging face token (Inputs will not be displayed): "))

local_folder = os.path.dirname(__file__)
repo_id = "Daibl/Voice"
# (Remember to enter the path to the files)
# To run the tts model you need: 
# a model like -> model_file.pth 
# and the associated config file in the same dir -> config.json
# Be aware that a directory named after the path in filename is being created to store the files
filename = ["tts_models--de--thorsten--vits/model_file.pth", "tts_models--de--thorsten--vits/config.json"]

os.makedirs(name=local_folder, exist_ok=True)
for file in filename:
    hf_hub_download(repo_id=repo_id, filename=file, local_dir=local_folder)
    
logout()