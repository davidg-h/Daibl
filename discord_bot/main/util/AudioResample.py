import io
import wave
import librosa
import numpy as np
import pydub

def resample_alt(original_audio_data):
    # Angenommen, 'original_audio_data' enthält Ihre Roh-Audiodaten
    # Sie müssen diesen Teil entsprechend Ihrer Datenquelle anpassen
    original_audio_data = original_audio_data
    frame_rate = 48000  # Beispielwert, passen Sie ihn an Ihre Daten an
    channels = 2        # Beispielwert für Stereo, 1 für Mono
    sample_width = 2    # 2 Bytes (16-bit) pro Sample

    # Erstellen Sie ein AudioSegment-Objekt aus den Rohdaten
    audio = pydub.AudioSegment.from_file(io.BytesIO(original_audio_data), format="raw",frame_rate=frame_rate, channels=channels, sample_width=sample_width)

    # Konvertieren Sie das Audio in Mono, falls erforderlich
    audio = audio.set_channels(1)

    # Resampling auf 16 kHz
    audio = audio.set_frame_rate(16000)

    # Stellen Sie sicher, dass die Bit-Tiefe 16-bit PCM ist
    audio = audio.set_sample_width(2)  # 2 Bytes (16-bit) pro Sample

    # Speichern Sie das Audio als WAV-Datei
    audio.export("/nfs/scratch/students/nguyenda81452/project/dev/daibl/discord_bot/main/STT/input.wav", format="wav")


def resample_and_save(input_path, output_path, target_sr=16000):
        # Laden der Audiodatei
        audio, sr_orig = librosa.load(input_path, sr=None, mono=True)  # Mono und Original-Abtastrate

        # Resampling auf die Ziel-Abtastrate, falls notwendig
        if sr_orig != target_sr:
            audio = librosa.resample(y=audio, orig_sr=sr_orig, target_sr=target_sr)

        # Konvertieren in 16-Bit-Werte (normales WAV-Format)
        audio_int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)

        # Speichern der resampelten Audiodatei
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16 Bit
            wav_file.setframerate(target_sr)
            wav_file.writeframes(audio_int16.tobytes())