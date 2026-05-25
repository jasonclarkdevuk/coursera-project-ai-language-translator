# Import libraries for IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model

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

def speech_to_text(audio_binary):
    return None

def text_to_speech(text, voice=""):
    return None

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
