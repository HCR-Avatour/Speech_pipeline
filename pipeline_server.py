from flask import Flask, request
from flask_cors import CORS
from speech_pipeline import speech_pipeline
import time
import os

app = Flask(__name__)
# add cors support
CORS(app)

@app.route('/', methods=['POST'])
def index():
    return 'Speech Server is running', 200

@app.route('/synth', methods=['POST'])
def synth():
    try:
        print("Received request to synthesize text")
        # Assuming the file field name is 'audioFile'
        audio_file = request.files['audioFile']
        counter = request.form.get('fileCounter')
        file_path = './samples/'+ audio_file.filename      
        print(audio_file, file_path, counter,  file_path.split(".")[2])
        
        if file_path.split(".")[2] == "wav":
            print("Initial audio received !", audio_file.filename)
            return 'Initial audio received !' + audio_file.filename, 200
        
        # Save the file to the './samples' directory
        audio_file.save(file_path)
        print("File saved")

        try:
            # Process the file using your speech_pipeline function
            speech_pipeline(file_path)
            # delete the original file
            os.remove(file_path)
        except Exception as e:
            print(f"Error processing file with speech_pipeline: {str(e)}")
            os.remove(file_path)
            return 'Error processing file', 500

        return 'File successfully received and processed! on file: ' + file_path
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        os.remove(file_path)
        return 'Error processing file', 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
