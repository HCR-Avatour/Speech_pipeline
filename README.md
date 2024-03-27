# Speech Pipeline

## Description
This project is a speech pipeline that processes audio input and performs various speech-related tasks such as speech recognition and speech synthesis. This is the Speech-to-Text-to-Speech backend for the AI assistant ("Ava") of the Avatour project.

## Features
- Speech recognition: Convert spoken language into written text.
- Speech synthesis: Generate spoken output from written text.

1. Provide audio input to the speech pipeline.
2. Speech-to-Text inference on the user audio.
3. Forward user transcription to the LLM as input prompt for a conversation.
4. Text-to-Speech inference on the LLM response.
5. Return generated audio and text to the respective interface (VR or website).

![ai_pipeline_fin](https://github.com/HCR-Avatour/Speech_pipeline/assets/33195033/0fef1412-845c-4c34-8901-75bbd43eaf7c)


## Person responsible
Alexandra Neagu

## Notes
Working on Python <=3.11 (error for 3.12).

Developed in Docker Container. To run: `docker compose up --build -d`
