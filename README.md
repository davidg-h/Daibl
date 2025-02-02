<div align="center">

  <img src="assets/docs/docs_images/logo.png" width="20%" height="20%">
  
  # Daibl


[![python][python-shield]][python-url]
[![pytorch][pytorch-shield]][pytorch-url]
[![HuggingFace][HuggingFace-shield]][HuggingFace-url]
[![pycord][pycord-shield]][pycord-url]
[![Hotword][Hotword-shield]][Hotword-url]
[![whisper][whisper-shield]][whisper-url]
[![coqui][coqui-shield]][coqui-url]


</div>

---

<details>
<summary>Table of Contents</summary>

- [About the project](#about-the-project)
  - [Folder Structure](#folder-structure)
  - [Modules](#modules)
  - [Usage](#usage)
- [Setup Guide](#setup-guide)
- [Additional](#additional)
  - [Docker environment](#docker-environment-beta)
  - [Virtual environment](#virtual-environment-activation)
- [Evaluation](#evaluation)
- [Authors](#authors)
- [License](#license)
- [Remarks](#remarks)

</details>

## <u>About The Project</u>

Daibl is a university project to help students learn more about AI and their Technologies. The acronym Daibl stands for **D**iscord **AI** **B**ot **L**earning. Daibl is a bot inspired by Alexa which can answer general and TH Nuernberg related questions, to help students (especially new ones) navigate their school life easier.

### Folder structure

The folder structure should give a rough overview of the code base and make the project easier to understand.

```sh
📦assets # resources and assets to run the project
 ┣ 📂docs
 ┣ 📂ffmpeg_builds
 ┗ ...
📦discord_bot
 ┣ 📂main
 ┃  ┣ 📂Bot     # main Bot application
 ┃  ┣ 📂LLM     # Communicating module with Large-Language-Models
 ┃  ┣ 📂STT     # Module for live transcription (ASR)
 ┃  ┣ 📂TTS_Bot # Module for text-to-speech
 ┃  ┣ 📂scrap   # TODO add description Vincent
 ┃  ┣ 📂util    # Module for utilities
 ┃  ┗ 📜main.py # programm entry point
 ┗ 📜.env    # token and keys
 ```

### Modules

Modules are designed to be interchangeable, for example using different LLMs to generate text

#### Bot

This module contains the code to run the Discord bot. The Discord api pycord is used to create the bot and communicate with the application

#### LLM (Large-Language-Models)

This module focuses on communication with the LLM. Hugging Face serves as the interface for running LLMs. It is a popular platform that provides a comprehensive set of tools and libraries for working with natural language processing (NLP) models and it is particularly well-known for its support of large language models (LLMs).

For our project we built a pipeline with Hugging Face to load the LLM and adjust parameters. The model is loaded into the GPU to accelerate processing. For the LLM different versions of Llama 2 and Vicuna were used. Onced loaded we can prompt question/text to the model to let it generate an answer which will be further processed by the bot.

Both Models have only a 4k Context and should be replaced by models with greater context.

#### STT (Speech to text)


This module uses whisper to transcripe audio data from discord. The data is saved as a wav file and given to whisper to process. The transcriped text is then given to the TTS module.


#### Hotword-Detection (Voice activation)

The goal was to integrate a Hotword Detection with the Word "Daibl", that works parallel to the audio recording.
It was challenging to find existing code that could be easy integrated into our work, especially since the Hotword Detection "Snowboy" was discontinued and the "Picovoice" does not allow the creation of custom hotwords with made-up words not found in the dictionary.

For this purpose, we utilized another GitHub repository "EfficientWord-Net"
[https://github.com/Ant-Brain/EfficientWord-Net](https://github.com/Ant-Brain/EfficientWord-Net).
However, this came with its own set of challenges, including poor performance, outdated Code and a lack of updates. Moreover, it only works only with MicStream via Python.
It was not possible to combine the Speech to Text live transcripe with the Hotword Detection. Despite these challenges, we plan to include the modified version in our repository.

The solution works adequately if used without live transcription or other simultaneous processes. However, it requires the implementation of sleep timers in some methods to function correctly; without them, the detection does not work.

The repository allows the creation of a custom reference file, which requires recording the desired hotword. We made 2-3 recordings of the word "Daibl" and saved them as a .json reference file.

In order to create these files, check out "EfficientWord-Net" Repo for Instructions. But use the fixed Code in our Repository.

- For using our Version of the Hotword Detection: import the method hw_detection from detection.py. It checks a given wav_file for the Hotword that is saved in the reference_file. The threshold can be changed for lower/higher "true chance"

```sh
def hw_detection(wav_file):
    daibl_hw = HotwordDetector(
        hotword="daibl",
        model=base_model,
        reference_file=os.path.join(PROJECT_PATH, "Hotword/wakewords/daibl/daibl_ref.json"),
        threshold=0.7,
        relaxation_time=2
    )
```

#### TTS_Bot (Text to speech)

TTS_Bot handles the training/finetuning of voice models as well as generating the voice to speak with the user. The text is processed by the voice model and saved to a wav file which is being played over the voice channel to the user.

To read more about the TTS setup click [this](assets/docs/TTS_Voice.md).

To run the voice model Coqui.ai TTS is being used. Coqui.ai TTS is a library for advanced Text-to-Speech generation. The platform offers pretrained models for over 1100 languages, along with tools for training new models and fine-tuning existing ones in any language. Additionally, it provides utilities for dataset analysis and curation.

#### Scrap

Scrap is all about the data used for the Retrieval Augmented Generation (RAG).
It has Notebooks for scraping the raw html data from the th-nuernberg website and the intranet website.
It features the data manipulation and preparation for the Retrival step.
Finally all the Methodes for creating Embeddings from the data and searching them is located here.

For more information on how to use and improve the code view this [README](assets/docs/Scrap.md).



### Usage

To start the Discord-Bot Daibl you need to have a Discord-Bot in Discord-Developer Portal. Also you need to use your own Discord Tokens of the Bot as seen in the Setup Guide. 

After the Setup you can start the main.py and the Bot will come Online. You can join a Voice Channel in Discord and write our Commands in a Text-Channel. The Bot will join in your current Voice-Channel and answer in the Text-Channel.

We implemented two Commands that start with the char "$"

- $daibl (Followed by the Question you want to ask him): You ask the Bot a Question and he will give you the Answer

<div>
  <img src="assets/docs/docs_images/Command1.png">
</div>

- $listen: The Bot will listen to your spoken Audio and will give you an Answer

<div>
  <img src="assets/docs/docs_images/Command2.png">
</div>


## <u> Setup Guide </u>

<div align="center">
  <img src="assets/docs/docs_images/clone_project.gif">
</div>

- Clone the repository:

```sh
mkdir daibl
cd daibl
git clone https://git.informatik.fh-nuernberg.de/devpsoft_studios/daibl.git
```

or

```sh
cd existing_repo
git remote add origin https://git.informatik.fh-nuernberg.de/devpsoft_studios/daibl.git
git branch -M main
```

- Create a $`\textcolor{red}{\text{.env file}}`$ in the [root of the project](/) and set the environment variables: (read the [remarks](#remarks) after creating the file)

```sh
# .env example
DISCORD_TOKEN=<your_token>
DISCORD_GUILD=<guild_or_server_name>
HUGGINGFACEHUB_API_TOKEN=<your_api_token>
PROJECT_PATH=<path/to/project> # Full path to project to simplify imports (if you want to read further into this google Python Path)
DATABASE_PATH=<path/to/database_of_context_documents>
```

The Hugging Face api token is used to get access to the [Hugging Face Hub](https://huggingface.co/docs/hub/index) and the [Hugging Face Ecosystem](https://huggingface.co/docs). For example: You can easily download different LLMs and Datasets with access through the api token in your python script. This makes automation and handling of ML components easier.

(Optional: To customize your Hugging Face environment follow [this manual](https://stackoverflow.com/questions/63312859/how-to-change-huggingface-transformers-default-cache-directory) and this [cache setup](https://huggingface.co/docs/transformers/installation?highlight=transformers_cache#cache-setup).)

- Create a [virtual environment](#virtual-environment-activation) and install the requirements

  ***(install the scraping_requirements if you intend to do web scraping)***

- [Download voice models](https://huggingface.co/Daibl/Voice) or use existing ones -> Change the [necessary paths](discord_bot/main/TTS_Bot/DaiblVoice.py) to use the models.

  ***Note: you can use the [download script](assets/models/tts-models/download_voice.py) for the voice models***

- [Download ffmpeg with our script](assets/ffmpeg_builds/download_ffmpeg.py) or [manually](https://ffmpeg.org/download.html). FFMPEG is needed for audio processing used in STT and TTS

## <u> Additional </u>

### Docker environment (beta)

The discord bot should be runable in any environment. For this purpose we use Docker. So file paths may be different when running on Windows. Devs should read through our [Docker documentation](assets/docs/Docker.md) to work on the project with docker.

### **Virtual environment activation**

The virtual environment is used to make developing easier and to only install the needed dependencies. To setup the virtual environment look into the corresponding [virtual environment documentation](assets/docs/Venv.md)

## <u> Evaluation </u>

The Evaluation of the RAG is handled in the Evaluation folder.
There are 3 different ascpects which are evaluated:

- the model (llama-13b, vicuna-13b, vicuna-70b)
- the embedding methode (tf-idf, MINI-LM-L6-v2)
- the context size (1, 5, 10 documents)

These aspects are evaluated in all combinations across 5 different answers.
The results can be viewed in the [excel table](assets/docs/Evaluation.xlsx).
The LLama2 Model with TF-IDF and 5 Context Documents is working best.
The Context is cut of earlier than 10 context documents maybe resulting in confusing the models.
One could expect Vicuna70b to be better, because it is a bigger model, but llama2 is newer and giving better results.

The results here may be biased by the selection of Questions or other factors like hyperparameters, or errors in generation.
For future evaluations we found some tips to improve:

This evaluation can be improved by:
- improving questions: assuring that there is indeed information to answere each questions
- categorising the questions in easy to hard and across different subjects
- using different llms with larger context (example Vicuna and Llama with 16k Context)
- don't cut off context documents
- don't cut off answers
- prompt engineer for better answers
- restructure code using the evaluation from langchain
- MINI_LM use all the data (including intranet)
- Having every model use same Temperature and hyperparameters

## <u> Authors </u>

[@David](https://github.com/davidg-h)
[@Vincent](https://github.com/firevince)
[@Patrick](https://github.com/DieserPat)
[@Elisabeth](https://github.com/elisabethvolkinshtein)

## <u> License </u>

Click [here](/LICENSE) to read the license.

---

---

---

## Remarks

You must adjust paths in some files / python scripts. For example the [tts-training-file line 35](discord_bot/main/TTS_Bot/Train_Voice/Training_Scripts/train_vits_win.py).

**In general:**
Every time the user/developer has to make a change for path reasons it will be marked as

```sh
# !!Change!! ...
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- https://shields.io/badges (Bagde generator) -->
<!-- https://github.com/Ileriayo/markdown-badges -->
[python-shield]: https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white
[python-url]: https://www.python.org

[pytorch-shield]: https://img.shields.io/badge/PyTorch-latest-EE4C2C.svg?style=flat&logo=pytorch
[pytorch-url]:https://pytorch.org

[HuggingFace-shield]: https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-latest-orange
[HuggingFace-url]: https://huggingface.co/

[pycord-shield]: https://img.shields.io/badge/Pycord-voice-neongreen?logo=discord&logoColor=white
[pycord-url]: https://docs.pycord.dev/en/stable/

[whisper-shield]: https://img.shields.io/badge/Whisper-74aa9c?logo=openai&logoColor=white
[whisper-url]: https://github.com/openai/whisper

[coqui-shield]: https://img.shields.io/badge/%F0%9F%90%B8Coqui.ai_TTS-green
[coqui-url]: https://github.com/coqui-ai/TTS

[Hotword-shield]: https://img.shields.io/badge/Hotword-git-orange
[Hotword-url]: https://github.com/Ant-Brain/EfficientWord-Net