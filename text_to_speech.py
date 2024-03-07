from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

def get_audio_from_text(text, file_path):
    try:
        inputs = processor(text=text, return_tensors="pt")
        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        sf.write(file_path, speech.numpy(), samplerate=16000)
        return speech
    except Exception as e:
        print(f"\nget_audio_from_text Error:: {e}\n")
        return None
    
if __name__ == "__main__":
    inputs = processor(text="Hello, my dog is cute.", return_tensors="pt")

    # load xvector containing speaker's voice characteristics from a dataset
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    sf.write("samples/speech.wav", speech.numpy(), samplerate=16000)

    # https://huggingface.co/datasets/Matthijs/cmu-arctic-xvectors
