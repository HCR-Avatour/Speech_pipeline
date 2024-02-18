from flask import Flask
from flask_cors import CORS
from speech_pipeline import speech_pipeline

app = Flask(__name__)
# add cors support
CORS(app)

@app.route('/synth', methods=['POST'])
def hello():
    print("Hello from the React app!")
    speech_pipeline("samples/audio.webm")
    return 'Hello from the server!'

if __name__ == '__main__':
    app.run(debug=True)
