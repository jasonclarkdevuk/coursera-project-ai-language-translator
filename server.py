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

# Posted speech audio is transcribed and returned
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    audio_binary = request.data # Get user's speech from the request

    # Call STT function to transcribe the speech using API
    stt = speech_to_text(audio_binary)

    # Return the response back
    # Create bespoke JSON response 
    response = app.response_class(
        response=json.dumps({"text": stt}), # Create simple JSON using dict using actual STT data 
        status=200, # Success response
        mimetype="application/json" # Format of response as JSON
    )

    return response

# Accept a user's message in text form with a selected preferred voice
# Message is processed and translated, converted back to speech
@app.route('/process-message', methods=['POST'])
def process_message_route():
    # Get user's message from request
    user_message = request.json["userMessage"]

    # Get user's preferred voice to be used for TTS
    voice = request.json["voice"]

    # Process user message
    watsonx_response_text = watsonx_process_message(user_message)

    # Remove any empty lines
    watsonx_response_text = os.linesep.join([s for s in watsonx_response_text.splitlines() if s])

    # Convert translation response into speech
    watsonx_response_speech = text_to_speech(watsonx_response_text, voice)

    # Encode as a Base64 string so it can be sent back in the JSON response
    watsonx_response_speech = base64.b64encode(watsonx_response_speech).decode("utf-8")

    # Send JSON response back containing the translation text and speech data
    # Create bespoke JSON response
    response = app.response_class(
        response=json.dumps({"watsonxResponseText": watsonx_response_text,"watsonxResponseSpeech": watsonx_response_speech}),
        status=200, # Success response
        mimetype="application/json" # Format of response as JSON
    )

    return response

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
