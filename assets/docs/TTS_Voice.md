# Train own voice for TTS model

ref tutorial:<https://www.youtube.com/playlist?list=PL19C7uchWZeo-j9mUmYeVfgzbP3vHSHU->

audio recording tool: <https://github.com/MycroftAI/mimic-recording-studio>

for windows there might be an issue with hosting it locally in a windows machine you have two options:

1. (Recommended) Download docker and run the recording tool in a docker container
2. The issue involves audio files not being safed by default. It could be because of missing ffmpeg support. Download and set ffmpeg in PATH in the environment variables and try again.

https://www.youtube.com/watch?v=bJjzSo_fOS8

TODO: finish doc for TTS