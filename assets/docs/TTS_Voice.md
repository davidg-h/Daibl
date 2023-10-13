# Train own voice for TTS model

ref tutorial series on voice cloning:

- general tutorial: <https://www.youtube.com/playlist?list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU->

- windows tutorial: <https://www.youtube.com/watch?v=bJjzSo_fOS8>

audio recording tool: <https://github.com/MycroftAI/mimic-recording-studio> [^1]

[^1]: read the remark

---

## Remark

For windows users there might be an issue with hosting mimic-recording-studio locally in a windows machine.

You have two options:

1. (Recommended) Download docker and run the recording tool in a docker container. Go to the directory with the tool in it and start docker
2. The issue involves audio files not being safed by default. It could be because of missing ffmpeg support. Download and set ffmpeg in PATH in the environment variables and try again.

Folder Structure for Training: (.wav files must be in mono, 22kHz frequency [22050 Hz], 16 bit)
dataset
-----wavs
----------audio.wav
-----metadata.cvs
