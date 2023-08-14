from TTS.api import TTS

# Running a multi-speaker and multi-lingual model
print(TTS.list_models())

# List available 🐸TTS models and choose the first one
model_name = TTS.list_models()[1]
print(model_name)
# Init TTS
tts = TTS(model_name)