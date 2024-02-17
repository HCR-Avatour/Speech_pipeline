import speech_to_text
import text_to_speech
import time

output_wav_file = "samples/Recording2.wav"
pipeline_file = "samples/pipeline.wav"

speech_to_text.record_audio(output_wav_file)
speech_to_text.play_audio(output_wav_file)
time.sleep(5)

transcription = speech_to_text.speech_to_text(output_wav_file)
print("Transcription of original: ", transcription)

speech = text_to_speech.get_audio_from_text(transcription, pipeline_file )
speech_to_text.play_audio(pipeline_file)