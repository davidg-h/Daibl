from multiprocessing import Process
from multiprocessing.managers import BaseManager

from time import sleep
from STT.LiveTranscripe import LiveTranscription


def work(stt:LiveTranscription, audio_model):
        stt.transcripe(audio_model)
    
def post_transcription(stt:LiveTranscription):
    
    timer = 10
    cached_transcription = ['']
    while timer > 0:
        current_transcription = stt.get_transcription()
        
        if cached_transcription != current_transcription:
            for line in current_transcription:
                if line not in cached_transcription:
                    print("Transcription:    " + line)
            cached_transcription = current_transcription
        
        timer -= 1
        sleep(1)
    
def run(whisper_model):
    
    BaseManager.register('LiveTranscription', LiveTranscription)
    with BaseManager() as manager:
        
        print("Init LiveTranscription")
        instance:LiveTranscription = manager.LiveTranscription()
        
        print("Main    : starting background process for STT-LiveTranscription")
        p = Process(target=work, args=[instance, whisper_model])
        
        print("Main    : running thread " + p.name)
        p.start()
        
        print(f"Posting transcription in channel ")
        LiveTranscription.post_transcription(instance)