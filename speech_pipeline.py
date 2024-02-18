import speech_to_text
import text_to_speech
import time
import os

# Accepted file formats: wav, ogg, flac
recording_file = "samples/Recording2.wav"
pipeline_file = "samples/pipeline.wav"
test_react = "samples/audio.wav"

def speech_pipeline(file_path):
    print("Speech Pipeline")
    # wait until file is created
    while not os.path.exists(file_path):
        time.sleep(1)
    wav_file = speech_to_text.webm_to_wav(file_path)
    transcription = speech_to_text.speech_to_text(wav_file)
    print("Transcription of original: ", transcription)
    
    output_file = wav_file.split(".")[0] + "_pipeline.wav"
    speech = text_to_speech.get_audio_from_text(transcription, output_file)
    speech_to_text.play_audio(output_file)
    # delete the original file
    os.remove(file_path)
    os.remove(wav_file)


if __name__ == "__main__":
    print("Speech Pipeline")
    print("1. Record audio ")
    # speech_to_text.record_audio(recording_file)
    print("2. Play audio")
    speech_to_text.play_audio(test_react)
    time.sleep(5)
    print("3. Transcribe audio")
    transcription = speech_to_text.speech_to_text(test_react)
    print("Transcription of original: ", transcription)
    print("4. Convert text to speech")
    speech = text_to_speech.get_audio_from_text(transcription, pipeline_file)
    speech_to_text.play_audio(pipeline_file)