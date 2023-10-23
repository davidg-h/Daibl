import os
import shutil

from trainer import Trainer, TrainerArgs

from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor


def main(name:str):
    '''
    Setup and start training/fine-tuning of Model. Look up the docs to restart training at a checkpoint.
    
    ...
    
    Parameters
    ----------
    name (str): Name of your model
    '''
    output_path = os.path.join("/nfs/scratch/students/nguyenda81452/itp/daibl/assets/models/tts-models", name) # folder where model is saved, change accordingly
    dataset_config = BaseDatasetConfig(
            formatter="thorsten",
            meta_file_train="metadata.csv",
            path="/nfs/scratch/students/nguyenda81452/itp/daibl/discord_bot/main/TTS_Bot/Train_Voice/Dataset_Generation/dataset/LJSpeech-1.1_David_dataset" # Change to your dataset
        )

    audio_config = VitsAudioConfig(
        sample_rate=22050,
        win_length=1024,
        hop_length=256,
        num_mels=80,
        mel_fmin=0,
        mel_fmax=None,
    )

    config = VitsConfig(
        audio=audio_config,
        run_name=f"vits_{name}-voice",
        batch_size=32,
        eval_batch_size=16,
        batch_group_size=5,
        num_loader_workers=0,
        num_eval_loader_workers=4,
        run_eval=True,
        test_delay_epochs=-1,
        epochs=1000,
        text_cleaner="phoneme_cleaners",
        use_phonemes=True,
        phoneme_language="de",
        phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
        compute_input_seq_cache=True,
        print_step=25,
        print_eval=True,
        mixed_precision=True,
        output_path=output_path,
        datasets=[dataset_config],
        test_sentences=[
            "Es hat mich viel Zeit gekostet ein Stimme zu entwickeln, jetzt wo ich sie habe werde ich nicht mehr schweigen.",
            "Sei eine Stimme, kein Echo.",
            "Es tut mir Leid David. Das kann ich leider nicht machen.",
            "Dieser Kuchen ist großartig. Er ist so lecker und feucht.",
            "Vor dem 22. November 1963.",
        ],
        #eval_split_size=0.14285714285714285, # assert error 'eval_split_size' parameter to a minimum of 0.14285714285714285
    )

    # INITIALIZE THE AUDIO PROCESSOR
    # Audio processor is used for feature extraction and audio I/O.
    # It mainly serves to the dataloader and the training loggers.
    ap = AudioProcessor.init_from_config(config)

    # INITIALIZE THE TOKENIZER
    # Tokenizer is used to convert text to sequences of token IDs.
    # config is updated with the default characters if not defined in the config.
    tokenizer, config = TTSTokenizer.init_from_config(config)

    # LOAD DATA SAMPLES
    # Each sample is a list of ```[text, audio_file_path, speaker_name]```
    # You can define your custom sample loader returning the list of samples.
    # Or define your custom formatter and pass it to the `load_tts_samples`.
    # Check `TTS.tts.datasets.load_tts_samples` for more details.
    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )

    # init model
    model = Vits(config, ap, tokenizer, speaker_manager=None)

    # init the trainer and 🚀
    trainer = Trainer(
        TrainerArgs(),
        config,
        output_path,
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )
    trainer.fit()
    print("Fertig!")


""" # Deprecated
def copy_dataset(): 
    cwd = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(cwd, "dataset")

    if os.path.exists(dst):  # if dataset folder exists remove it and copy new dataset
        shutil.rmtree(dst)

    shutil.copytree(
        #src="discord_bot\main\TTS_Bot\Train_Voice\Dataset_Generation\dataset",
        src="itp/daibl/discord_bot/main/TTS_Bot/Train_Voice/Dataset_Generation/dataset", # th-server
        dst=dst,
    )
    print("Dataset Copied Successfully") """


#_ = copy_dataset() if input("Copy dataset from the 'Dataset_Generation' folder? (y/n):   ") == 'y' else print("") # comment out if not needed
main("david-tts") # Change the name of your model