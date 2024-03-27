# Speech Pipeline

## Description
This project is a speech pipeline that processes audio input and performs various speech-related tasks such as speech recognition and speech synthesis. This is the Speech-to-Text-to-Speech backend for the AI assistant ("Ava") of the Avatour project.

## Features
- Speech recognition: Convert spoken language into written text.
- Speech synthesis: Generate spoken output from written text.

## Usage
1. Provide audio input to the speech pipeline.
2. Speech-to-Text inference on the user audio.
3. Forward user transcription to the LLM as input prompt for a conversation.
4. Text-to-Speech inference on the LLM response.
5. Return generated audio and text to the respective interface (VR or website).

Working on Python <=3.11 (error for 3.12).
