import speech_to_text
import text_to_speech
import llm_local
import time
import os

# Accepted file formats: wav, ogg, flac
recording_file = "samples/Recording2.wav"
pipeline_file = "samples/pipeline.wav"
test_react = "samples/audio.wav"

def speech_pipeline(file_path):
    print("Speech Pipeline...")

    wait_until_file_exists(file_path)
    
    if file_path.split(".")[1] != "wav": 
        wav_file = speech_to_text.webm_to_wav(file_path)
        print("Wav file: ", wav_file)
    
        wait_until_file_exists(wav_file)
        
        transcription = speech_to_text.speech_to_text(wav_file)
        print("Transcription of original: ", transcription)
    else:
        transcription = speech_to_text.speech_to_text(file_path)
        print("Transcription of original: ", transcription)
    
    print("Passing to LLM...")
    llm_response = llm_local.callLLM(transcription)
    print("LLM response: ", llm_response)
    
    output_file = file_path.split(".")[0] + "_pipeline.wav"
    print("Output file: ", output_file, " from ", file_path)
    speech = text_to_speech.get_audio_from_text(llm_response, output_file)
    speech_to_text.play_audio(output_file)

    if file_path.split(".")[1] != "wav":
        # if we want to remove the wav audio
        os.remove(wav_file)
    
def wait_until_file_exists(file_path):
    time_count = 0
    while not os.path.exists(file_path) :
        print("Waiting for file: ", file_path)
        time.sleep(1)
        if time_count == 5:
            print("File not found: ", file_path)
            return
        time_count+=1
    return "wait_until_file_exists: Error on opening file "+ file_path

if __name__ == "__main__":
    # print("Speech Pipeline")
    # print("1. Record audio ")
    # # speech_to_text.record_audio(recording_file)
    # print("2. Play audio")
    # speech_to_text.play_audio(test_react)
    # time.sleep(5)
    # print("3. Transcribe audio")
    # transcription = speech_to_text.speech_to_text(test_react)
    # print("Transcription of original: ", transcription)
    # print("4. Convert text to speech")
    # speech = text_to_speech.get_audio_from_text(transcription, pipeline_file)
    # speech_to_text.play_audio(pipeline_file)
    speech_pipeline(pipeline_file)