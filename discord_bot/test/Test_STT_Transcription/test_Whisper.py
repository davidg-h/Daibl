import whisper
import sys
import os

class add_path():
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old_path = os.environ['PATH']
        os.environ['PATH'] = self.path + os.pathsep + self.old_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ['PATH'] = self.old_path

with add_path(r'discord_bot\\TTS_Bot\\ffmpeg-6.0-full_build\\bin'):        
    cwd = os.path.dirname(os.path.abspath(__file__))

    model = whisper.load_model("base")
    result = model.transcribe(cwd + '\\Question.mp3')
    print(result["text"])
