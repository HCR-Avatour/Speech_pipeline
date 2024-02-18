import * as React from 'react';
import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';

export default function RecordComponent() {

  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/synth', {
        method: 'POST',
      });

      if (response.ok) {
        console.log('Server response:', await response.text());
      } else {
        console.error('Failed to communicate with the server');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const addAudioElement = (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;
    // audio.duration = recorderControls.recordingTime; //read only
    console.log('audio.duration: ', audio.duration); //NaN ????
    // document.body.appendChild(audio);
    handleButtonClick();
  };

  // TODO: check how to get the audio duration for ffmpeg to not error when calling the python functions
  const recorderControls = useAudioRecorder(
    {
      noiseSuppression: true,
      echoCancellation: true,
    },
    (err) => console.table(err) // onNotAllowedOrFound
  );

  return (
    <div>
      <AudioRecorder
        onRecordingComplete={addAudioElement}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
          // autoGainControl,
          // channelCount,
          // deviceId,
          // groupId,
          sampleRate: 16000,
          // sampleSize,
        }}
        onNotAllowedOrFound={(err) => console.table(err)}
        downloadOnSavePress={true}
        downloadFileExtension="wav" // for mp3 and wav, must set cross origin isolation
        mediaRecorderOptions={{
          audioBitsPerSecond: 128000,
        }}
        showVisualizer={true}
        recorderControls={recorderControls}
      />
      <br />
      {recorderControls.recordingTime}
    </div>
  );
}