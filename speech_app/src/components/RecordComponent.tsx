import * as React from 'react';
import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';

export default function RecordComponent() {

  const [audioBlob, setAudioBlob] = React.useState<Blob>(new Blob());
  const [counter, setCounter] = React.useState(0);
  // React.useEffect(() => {
  //   initialiseSpeechPipeline();
  //   setCounter(counter + 1);
  // }, []);

  // const initialiseSpeechPipeline = async () => {
  //   try {
  //     const initial_audio = await fetch('./audio/audio.wav');
  //     const blob = await initial_audio.blob();
  //     const formData = new FormData();
  
  //     // Assuming your blob is named 'audioBlob', adjust accordingly
  //     formData.append('audioFile', blob, 'audio'+counter+'.wav');
  //     formData.append('fileCounter', counter.toString());

  //     console.log('Sending audio to server ', 'audio'+counter+'.wav');
  //     const response = await fetch('http://localhost:5000/synth', {
  //       method: 'POST',
  //       body: formData
  //       }
  //     );
  
  //     if (response.ok) {
  //       console.log('Server response:', await response.text());
  //     } else {
  //       console.error('initialiseSpeechPipeline Failed to communicate with the server');
  //     }
  //   } catch (error) {
  //     console.error('Error:', error);
  //   }
  // };

  const handleButtonClick = async () => {
    try {
      const formData = new FormData();
  
      // Assuming your blob is named 'audioBlob', adjust accordingly
      formData.append('audioFile', audioBlob, 'audio'+counter+'.webm');
      formData.append('fileCounter', counter.toString());

      console.log('Sending audio to server ', 'audio'+counter+'.webm');
      const response = await fetch('http://localhost:5000/synth', { // update IP here with container IP (if run in wsl, get wsl ip through "wsl hostname -I")
        method: 'POST',
        body: formData
        }
      );
  
      if (response.ok) {
        console.log('Server response:', await response.text());
      } else {
        console.error('handleButtonClick Failed to communicate with the server');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const addAudioElement = (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    // const audio = document.createElement('audio');
    // audio.src = url;
    // audio.controls = true;
    // console.log('Audio duration:', audio.duration);
    setAudioBlob(blob);

    // Call the speech_pipeline API
    handleButtonClick();
    setCounter(counter + 1);
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
        downloadOnSavePress={false}
        downloadFileExtension="webm" // for mp3 and wav, must set cross origin isolation
        mediaRecorderOptions={{
          audioBitsPerSecond: 128000,
        }}
        showVisualizer={true}
        recorderControls={recorderControls}
      />
      {/* <br /> */}
      {/* {recorderControls.recordingTime} */}
    </div>
  );
}