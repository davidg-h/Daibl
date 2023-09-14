#! python3.7

import io
import os
import shutil
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from multiprocessing import Queue
import tempfile 
import time
from sys import platform

from util.Environment import add_path
from types import SimpleNamespace


class LiveTranscription:
    """
    # Handles the live transcription of ASR
    
    ...
    
    Attributes
    ----------
    model : str
        Model to use: choices=["tiny", "base", "small", "medium", "large"]
    non_english : bool
        Don't use the english model. -> TRUE
    energy_threshold : int
        Energy level for mic to detect.
    record_timeout : float
        How real time the recording is in seconds.
    phrase_timeout : float
        How much empty space between recordings before we consider it a new line in the transcription.
    default_microphone : str
        Default microphone name for SpeechRecognition. Run this with 'list' to view available Microphones.
    """
    def __init__(self, model="medium", non_english=True, energy_threshold:int=1000, record_timeout:float=2, phrase_timeout:float=3, default_microphone='pulse'):
            
            self.cwd = os.path.dirname(__file__)
            self.tmp_dir = os.path.join(self.cwd, "tmp")
            
            
            self.args = SimpleNamespace(**{
                'model':model, 
                'non_english':non_english, 
                'energy_threshold':energy_threshold, 
                'record_timeout':record_timeout, 
                'phrase_timeout':phrase_timeout,
                'default_microphone': ''
                })
            
            if 'linux' in platform:
                self.args.default_microphone = default_microphone
            
            # The last time a recording was retreived from the queue.
            self.phrase_time = None
            # Current raw audio bytes.
            self.last_sample = bytes()
            # Thread safe Queue for passing data from the threaded recording callback.
            self.data_queue = Queue()
            # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
            self.recorder = sr.Recognizer()
            self.recorder.energy_threshold = self.args.energy_threshold
            # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
            self.recorder.dynamic_energy_threshold = False

            self.record_timeout = self.args.record_timeout
            self.phrase_timeout = self.args.phrase_timeout
            
            self.transcription = ['']
            
            self.audio_model = self.load_model()
    
    def mic(self):
        """
        Returns the microphone for speech recognition
        
        \b
        Important for linux users. 
        Prevents permanent application hang and crash by using the wrong Microphone
        """
        if 'linux' in platform:
            mic_name = self.args.default_microphone
            if not mic_name or mic_name == 'list':
                print("Available microphone devices are: ")
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Microphone with name \"{name}\" found")   
                return
            else:
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    if mic_name in name:
                        return sr.Microphone(sample_rate=16000, device_index=index)
        else:
            return sr.Microphone(sample_rate=16000)
    
    def load_model(self):
        """ Load whisper model """
        model = self.args.model
        if self.args.model != "large" and not self.args.non_english:
            # load only english model 
            model = model + ".en"
        # check for cuda (nvidia graphic card) availability
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        audio_model = whisper.load_model(model).to(device)
        print("Model loaded.\n")
        return audio_model
    
    def get_transcription(self):
        return self.transcription
    
    def create_tmp_dir(self):
        """ creates temp directory in current directory of file """
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
            
    def del_tmp_dir(self):
        """ removes the temp directory """
        shutil.rmtree(self.tmp_dir)
        print("Deleting temporary directory -> Done")
        
    def record_callback(self, _, audio:sr.AudioData) -> None:
                """
                Threaded callback function to recieve audio data when recordings finish.
                audio: An AudioData containing the recorded bytes.
                """
                # Grab the raw bytes and push it into the thread safe queue.
                data = audio.get_raw_data()
                self.data_queue.put(data)
                
    def line_to_post(self):
        """
        concatinates all of the transcription in one line
        """
        cached_transcription = ['']
        current_transcription = self.get_transcription()
        line_to_post = ""
        
        if cached_transcription != current_transcription:
            for line in current_transcription:
                if line not in cached_transcription:
                    line_to_post += line + " "
            cached_transcription = current_transcription
            
        return line_to_post
                
    async def transcripe(self, audio_model, channel):
        """ live transcription using speech recognition and whisper """
        self.create_tmp_dir()
        source = self.mic()
        
        # reset transcription attributes to default before every transcript
        self.data_queue = Queue()
        msg = None
        self.transcription = ['']
        
        temp_file =  tempfile.NamedTemporaryFile(mode='w+b' , dir=self.tmp_dir, delete=False)
        temp_file.close()
        
        with source:
            self.recorder.adjust_for_ambient_noise(source)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        stop_listening = self.recorder.listen_in_background(source, self.record_callback, phrase_time_limit=self.record_timeout)

        # Cue the user that we're ready to go.
        print("Live-Transcription started. Please say something.\n")
        await channel.send("Live-Transcription started. Please say something.", delete_after=4)
        
        # record only 15 sec of live audio for transcription
        t_end = time.time() + 15
        while time.time() < t_end:
            try:
                now = datetime.utcnow()
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty():
                    phrase_complete = False
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        self.last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    self.phrase_time = now

                    # Concatenate our current audio data with the latest audio data.
                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data

                    # Use AudioData to convert the raw data to wav data.
                    audio_data = sr.AudioData(self.last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    # Write wav data to the temporary file as bytes.
                    with open(temp_file.name, 'w+b') as f:
                        f.write(wav_data.read())

                    # Read the transcription.
                    with add_path("assets/ffmpeg-6.0-full_build/bin"):
                        with torch.cuda.device('cuda:0'):
                            result = audio_model.transcribe(temp_file.name, fp16=torch.cuda.is_available())
                    text = result['text'].strip()

                    # If we detected a pause between recordings, add a new item to our transcripion.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text

                    # Clear the console to reprint the updated transcription.
                    #os.system('cls' if os.name=='nt' else 'clear')
                    if msg != None:
                        await msg.delete()
                    msg = await channel.send("Live-Transcription:  " + self.line_to_post())
                    for line in self.transcription:
                        print(line)
                    # Flush stdout.
                    print('', end='', flush=True)

                    # Infinite loops are bad for processors, must sleep.
                    time.sleep(0.25)
            except Exception:
                break
        
        # stops background thread of audio recording
        stop_listening(True)
        await channel.send("Live-Transcription ended", delete_after=4)
        
        print("\n\nTranscription:")
        for line in self.transcription:
            print(line)
        
        self.del_tmp_dir()