import base64
import json
from flask import Flask, render_template, request
from flask_cors import CORS
import os

# Import functions for STT, TTS and translation processing
from worker import speech_to_text, text_to_speech, watsonx_process_message

# Create a Flask app
# __name__ directs Flask to look in current folder for resources
# CORS policy is set - for development purposes - any website or domain can make requests to the backend
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# First page of application, render main index page
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    return None

@app.route('/process-message', methods=['POST'])
def process_message_route():
    return None

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
