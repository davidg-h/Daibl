# Manual for training/finetune own voice for TTS model

---
-> | [Back](/README.md)
-|-

## Setup

You will need following requirements to make training/finetuning possible and easier:
- [mimic-recording-studio](https://github.com/MycroftAI/mimic-recording-studio): recording tool specialised for tts data generation [^1] (a version is already in daibl/assests/rec-tool/)
    - [setup of mimic-recording-studio](https://www.youtube.com/watch?v=tAuPAPdahvA&list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU-&index=2)
- [coqui-ai TTS](https://github.com/coqui-ai/TTS): repo to set up TTS and train/finetune own models (a version is already in daibl/assests/TTS-dev/)
    - [setup of coqui-ai TTS: Follow the Installation chapter](https://tts.readthedocs.io/en/dev/tutorial_for_nervous_beginners.html)
    - [alternative tutorial](https://www.youtube.com/watch?v=fXwVn02OesA&list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU-&index=5)

## Dataset Generation

The dataset follows the ljspeech folder structure: 
```sh
📦dataset # name of your dataset
 ┣ 📂wavs # containg all .wav files with unique names
 ┃  ┣ <GUID>.wav
 ┃  ┣ ....
 ┃  ┗ <GUID>.wav   
 ┗ 📜metadata.cvs # containing references of .wav files to spoken text
```
The explanation of the ljspeech structure and how to generate it from the data recorded with mimic-recording-studio can be found [here](https://www.youtube.com/watch?v=Vxq8FAoNzqY&list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU-&index=4) <br>
&rarr; the script is already there: daibl/discord_bot/main/TTS_Bot/Train_Voice/Dataset_Generation/MRS2LJSpeech.py

***MRS2LJSpeech.py ffmpeg flag is defaulted to True to convert any audio to the required format - In general pay attention that you start anything that needs ffmpeg with daibl/assets/ffmpeg-6.0-full_build/bin/ (look at how the util/Environment.py works)***

**Attention**: your data (.wav files) should have following format:
- mono
- 22kHz frequency [22050 Hz]
- 16 bit

***At your own risk:**<br>
You can also record the audio data on your own (without the tool mimic-recording-studio) if you follow the format and folder structure above.<br> 
It is recommended to install the free software audacity from https://www.audacityteam.org <br> 
**Caution: Dont´t download the software from audacity.de - the software could be compromised with malware***

## Train/Finetune model

Training/Finetuning a model is straight forward. You can either start the training on a model from scratch or use an existing model and finetune it. We recommend the last option as it is less time consuming.

For both options there are [already existing scripts](https://github.com/coqui-ai/TTS/tree/main/recipes). Take one recipe and adjust it to your needs.

### Train model from scratch

Go into the TTS_Bot module and run the train_vits_win.py script. <br>
Following parameters should be changed:
- output_path (Sets the path were your model is saved)
- path in dataset_config (specify a fully qualified path to **your dataset**)

Source: [coqui-ai TTS: Tutorial For Nervous Beginners](https://tts.readthedocs.io/en/dev/tutorial_for_nervous_beginners.html)

### Finetune model

For the german language we use a base model from [Thorsten-Voice](https://github.com/thorstenMueller/Thorsten-Voice/tree/master) which is located in: daibl/assets/models/tts-models/tts_models--de--thorsten--vits/

Start finetuning on the base model:
```sh
# cd into the location where the trainig script is or start the script with a qualified path
# start the script with the --restore_path flag (Attention: specify which model to restore from)
CUDA_VISIBLE_DEVICES="0" python daibl/discord_bot/main/TTS_Bot/Train_Voice/Training_Scripts/train_vits_win.py --restore_path /home/$USER/path-to-project/daibl/assets/models/tts-models/tts_models--de--thorsten--vits/model_file.pth
```

Continue a previous run:
```sh
# cd into the location where the trainig script is or start the script with a qualified path
# start the script with the --continue_path flag (Attention: Here only specify the folder)
CUDA_VISIBLE_DEVICES=0 python train_vits_win.py --continue_path /home/$USER/path-to-project/daibl/assets/models/tts-models/path/to/previous/run/folder/
```

Source: [coqui-ai TTS: Fine-tuning a 🐸 TTS model](https://tts.readthedocs.io/en/dev/finetuning.html#fine-tuning-a-tts-model)

## Other Sources and References

Tutorial series on voice cloning:

- general tutorial: <https://www.youtube.com/playlist?list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU->

- windows tutorial: <https://www.youtube.com/watch?v=bJjzSo_fOS8>

Training from Checkpoints: <https://www.youtube.com/watch?v=O6KxJR95WpE&list=PL19C7uchWZerUT0qIiEv7m2zXBs5kYl1L&t=878s>

Discussion on Recommendations for fine-tuning for custom voice: <https://github.com/coqui-ai/TTS/discussions/1208>

---
---

[^1]: Remark

For windows users there might be an issue with hosting mimic-recording-studio locally in a windows machine.

You have two options:

1. (Recommended) Download docker and run the recording tool in a docker container. Go to the directory with the tool in it and start docker
```sh 
docker-compose up
```
2. The issue involves audio files not being safed by default. It could be because of missing ffmpeg support. Download and set ffmpeg in PATH in the environment variables of your pc and try again.

---
---