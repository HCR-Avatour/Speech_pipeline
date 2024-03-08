import speech_to_text
import text_to_speech
import llm_local
import time
import os
import requests
import json

# Accepted file formats: wav, ogg, flac
recording_file = "./samples/Recording2.wav"
pipeline_file = "./samples/pipeline.wav"
test_react = "./samples/audio.wav"

url = 'https://assistant.avatour.duckdns.org' # to be changed to the avatour_web URL

def speech_pipeline(file_path):
    print("Speech Pipeline...")

    wait_until_file_exists(file_path)
    
    if file_path.split(".")[2] != "wav": 
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
    
    output_file = "."+file_path.split(".")[1] + "_pipeline.wav"
    print("Output file: ", output_file, " from ", file_path)
    speech = text_to_speech.get_audio_from_text(llm_response, output_file)  ## TESTING - works on ubuntu not on langchain image
    # speech_to_text.play_audio(output_file)
    
    # HTTP POST request to share the audio file to a server IP
    print("Sharing transcript and audio to server...")
    share_transcript_audio(llm_response, output_file, url) # sending llm TRANSCRIPT and AUDIO to JS website ## TESTING - works on ubuntu not on langchain image
    # share_transcript_audio(llm_response, pipeline_file, url) # sending llm TRANSCRIPT and AUDIO to JS website
    # share_transcript_audio("test Pipeline file", pipeline_file, url) # sending llm TRANSCRIPT and AUDIO to JS website
    
    # if file_path.split(".")[1] != "wav":
    #     # if we want to remove the wav audio
    #     os.remove(wav_file)
    
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

def share_transcript_audio(transcript, file_path, url):
    """
        HTTP POST request to share the transcript to a server IP
    """
    # print("share_transcript Transcript: ", transcript)
    # print("share_output_audio File path: ", file_path)
    
    json_transcript = {"transcript": transcript}
    files = {"audioFile": open(file_path, 'rb')}
    
    response = requests.post(url, data=json_transcript, files=files) #, files=files
    if response.status_code == 200:
        print('share_transcript Transcript successfully posted.')
    else:
        print(f'share_transcript Failed to post transcript. Status code: {response.status_code}')

if __name__ == "__main__":
    print("Speech Pipeline")
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
    # speech_pipeline(pipeline_file)
    share_transcript_audio("HI, TEST here!", test_react, url)
