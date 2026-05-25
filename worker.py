# Import libraries for IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model

# Import requests library for API calls
import requests

# Within learning environment, a Watson API Key is not needed
# Only project ID needs to be set in CloudIDE environment

# Placeholder Watsonx_API and Project ID in case the code needs to be used outside of learning environment
# API_KEY = "API KEY"
PROJECT_ID = "skills-network"

# Define IBM Cloud credentials
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
    # "apikey": API_KEY
}

# Define model that will be used for processing
# Mistral AI model is an open source LLM
MODEL_ID = "mistralai/mistral-medium-2505"

# Imports for model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

# Model parameters
# Since we are doing translation and do not need highly creative outputs, we set it to Greedy Search
# Greedy Search means the model will always pick the most likely next word
parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
model = Model(
    model_id=MODEL_ID,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)

# Audio data is received and passed to IBM Watsonx STT APIX
def speech_to_text(audio_binary):
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    # Set up parameters for HTTP request
    # Set language and acoustic model framework to US English
    # Expecting multimedia like audio / video tracks
    parameters = {
        "model": "en_US_Multimedia"
    }

    # Send HTTP POST request
    # Data body of audio binary data
    response = requests.post(
        api_url, params=parameters, data=audio_binary
    ).json()

    text = "null"

    # Check if 'results' exists and is not empty
    if response.get("results"):
        # Safely grab the last result and its last alternative transcript
        latest_result = response.get("results")[-1]
        text = latest_result.get("alternatives")[-1].get("transcript")

    return text

def text_to_speech(text, voice=""):
    # Set up Watson TTS HTTP API URL
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # If user has specified a voice, add parameter to API url
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    
    # Set headers for request
    headers = {
        "Accept": "audio/wav", # Send audio data in WAV format
        "Content-Type": "application/json" # Format of body of POST request is JSON        
    }

    # Set up request body
    json_data = {
        "text": text
    }

    # Send HTTP POST request   
    # Response is binary audio data in the content of response
    response = requests.post(api_url, headers=headers, json=json_data)

    return response.content

# Prompt is passed to Watsonx's Mistral API to a receive a response
def watsonx_process_message(user_message):
    # Set the prompt for the API
    # Prompt optimised for translating English -> Spanish
    prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.

    English: {user_message}
    Spanish:
    """

    response = model.generate_text(prompt=prompt)

    # Remove any leading or trailing spaces
    return response.strip() 
