from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
# from huggingface_hub import login
# login(token="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", add_to_git_credential=False)

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = None

########### record audio throgh microphone
import librosa
import time

import pyaudio
import wave
import pygame

def record_audio(file_name, duration=5, sample_rate=16000, channels=2, chunk_size=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio to a WAV file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def play_audio(file_name):
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    pygame.quit()

def speech_to_text(file_path, duration=5, sample_rate=16000):
    # Load the audio file
    # waveform, sample_rate = torchaudio.load(file_path)
    waveform, sample_rate = librosa.load(file_path, sr=None, mono=True)

    # Preprocess the audio file
    input_features = processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_features

    # Generate the token IDs
    predicted_ids = model.generate(input_features)

    # Decode the token IDs to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription

if __name__ == "__main__":
    output_wav_file = "samples/Recording2.wav"

    # record_audio(output_wav_file)
    # play_audio(output_wav_file)
    # time.sleep(5)
    
    transcription = speech_to_text(output_wav_file)
    print("Transcription: ", transcription)