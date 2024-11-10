import requests
from playsound import playsound  # or use pydub for more flexibility
import os

# Set up your API key and endpoint
API_KEY = "sk_a334942c47e004c54a6121dad7a0195cb4ade8508993aaae"
VOICE_ID = "CwhRBWXzGAHq8TQ4Fs17"  # Replace with the ID of the voice you want to use
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def speak_text(text):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # Set model as required
    }

    # Send request to ElevenLabs API
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        # Save audio to file
        audio_file = "output.mp3"
        with open(audio_file, "wb") as file:
            file.write(response.content)

        # Play the audio file
        playsound(audio_file)

        # Optional: Delete the file after playing
        os.remove(audio_file)
    else:
        print("Error:", response.status_code, response.text)


speak_text("Hello, this is an example of using ElevenLabs to speak text.")
