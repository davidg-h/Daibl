import os
import numpy as np
import wave
import time
from STT.Hotword.eff_word_net.engine import HotwordDetector
from STT.Hotword.eff_word_net.audio_processing import Resnet50_Arc_loss
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
PROJECT_PATH = os.getenv("PROJECT_PATH")
base_model = Resnet50_Arc_loss()
def hw_detection(wav_file):
    daibl_hw = HotwordDetector(
        hotword="daibl",
        model=base_model,
        reference_file=os.path.join(PROJECT_PATH, "discord_bot/main/STT/Hotword/wakewords/daibl/daibl_ref.json"),
        threshold=0.7,
        relaxation_time=2
    )

    # Open the WAV file
    with wave.open(wav_file, 'rb') as wf:
        frame_rate = wf.getframerate()
        if frame_rate != 16000:
            raise ValueError("Unsupported frame rate: {}".format(frame_rate))

        # Set the window length to 1.5 seconds (24000 frames at 16000 Hz)
        window_length_frames = 24000

        while True:
            frames = wf.readframes(window_length_frames)
            frame = np.frombuffer(frames, dtype=np.int16)
            time.sleep(2) 
            if len(frames) == 0:
                break  # End of file

            # If the frame is shorter than expected, pad it with zeros
            if frame.shape[0] < window_length_frames:
                frame = np.pad(frame, (0, window_length_frames - frame.shape[0]), 'constant')

            result = daibl_hw.scoreFrame(frame)
            if result is None:
                # no voice activity
                continue
            
            if result["match"]:
                return True

    return False