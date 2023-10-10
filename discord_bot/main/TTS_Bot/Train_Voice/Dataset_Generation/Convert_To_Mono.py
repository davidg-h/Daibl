import os
from pydub import AudioSegment

import sys
print(sys.path)
sys.path.append(r"/home/nguyenda81452/it_project/daibl/discord_bot/main")
print(sys.path)

from util.Environment import add_path

def convert():
    # Input and output folder paths
    wd = "/home/nguyenda81452/it_project/daibl/discord_bot/main/TTS_Bot/Train_Voice/Dataset_Generation/dataset/LJSpeech-1.1_David_dataset" # change to yours
    input_folder = wd + "/wavs" 
    output_folder = wd + "/wavs_mono"

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Sample rate for conversion
    target_sample_rate = 22050

    # List all WAV files in the input folder
    wav_files = [file for file in os.listdir(input_folder) if file.lower().endswith(".wav")]

    for wav_file in wav_files:
        input_path = os.path.join(input_folder, wav_file)
        output_path = os.path.join(output_folder, wav_file)

        # Load the stereo WAV file
        audio = AudioSegment.from_file(input_path)

        # Set the sample rate to 22050 Hz
        audio = audio.set_frame_rate(target_sample_rate)

        # Convert stereo to mono
        audio = audio.set_channels(1)

        # Export the mono audio to the output folder
        audio.export(output_path, format="wav")

        print(f"Converted {wav_file} to mono at {target_sample_rate} Hz")

    print("Conversion of all WAV files complete.")

with add_path("assets/ffmpeg-6.0-full_build/bin"):
    convert()