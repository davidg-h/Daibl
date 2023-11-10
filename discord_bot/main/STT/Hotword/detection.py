import os
from STT.Hotword.eff_word_net.streams import SimpleMicStream
from STT.Hotword.eff_word_net.engine import HotwordDetector

from STT.Hotword.eff_word_net.audio_processing import Resnet50_Arc_loss

from STT.Hotword.eff_word_net import samples_loc

base_model = Resnet50_Arc_loss()


def hw_detection():
    daibl_hw = HotwordDetector(
        hotword="daibl",
        model = base_model,
        reference_file=os.path.join(samples_loc, r"C:\Users\Patri\Desktop\Daibl\daibl\discord_bot\main\STT\Hotword\wakewords\daibl\daibl_ref.json"),
        threshold=0.7,
        relaxation_time=2
    )

    mic_stream = SimpleMicStream(
        window_length_secs=1.5,
        sliding_window_secs=0.75,
    )

    mic_stream.start_stream()

    print("Say daibl ")
    while True :
        frame = mic_stream.getFrame()
        result = daibl_hw.scoreFrame(frame)
        if result==None :
            #no voice activity
            continue
        if(result["match"]):
            return True
