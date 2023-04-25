import os
import io
import json
import requests
import openai
import speech_recognition as sr
import pygame
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Load API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("eleven_api_key")
CSE_ID = os.getenv("CSE_ID")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Voice settings. Find using the Playground get voices api
VOICE_ID = "YmsQAIBXwZz4TnWwMTzf"
STABILITY = 0.5
SIMILARITY_BOOST = 0.5


def listen():
    """Listens to the user's voice input and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
    except Exception as e:
        print("Sorry, I couldn't understand that.")
        return None

    return command


def elevenlabs_speak(text, voice_id, stability, similarity_boost, eleven_api_key):
    """Converts the given text to speech using ElevenLabs API and plays the audio."""
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "xi-api-key": eleven_api_key,
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    }

    response = requests.post(tts_url, json=data, headers=headers, stream=True)
    CHUNK_SIZE = 4096

    audio_data = io.BytesIO()
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_data.write(chunk)

    audio_data.seek(0)  # Reset the stream position to the beginning

    # Play the generated audio using an audio player of your choice.
    pygame.mixer.init()
    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    time.sleep(0.3)


def google_search(search_term, api_key, cse_id, **kwargs):
    """Performs a Google search using the given search term and returns the search results."""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def ask_openai(prompt):
    """Asks OpenAI GPT-3.5-turbo a question and returns the model's response."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()


def main():
    while True:
        print("Waiting for activation command...")
        command = listen()
        if command is None:
            continue

        command = command.lower()
        if "adam" in command or "adam power on" in command or "power on" in command:
            elevenlabs_speak("Hello Sir, how can I help you?", VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
            break

    while True:
        command = listen()
        if command is None:
            continue

        command = command.lower()

        if "search" in command or "search online" in command:
            query = command.replace("search", "").strip()
            search_results = google_search(query, GOOGLE_API_KEY, CSE_ID)
            items = search_results.get('items', [])

            if len(items) > 0:
                num_results = min(3, len(items))
                elevenlabs_speak(f"Here are the top {num_results} search results for {query}", VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
                for i, result in enumerate(items[:num_results]):
                    elevenlabs_speak(f"Result {i+1}: {result['title']}", VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
                    elevenlabs_speak(result['snippet'], VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
            else:
                elevenlabs_speak(f"Sorry, I couldn't find any search results for {query}", VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
        elif "exit" in command or "power down" in command or "thank you adam. power down" in command:
            elevenlabs_speak("Thank you.", VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)
            break
        else:
            response = ask_openai(command)
            elevenlabs_speak(response, VOICE_ID, STABILITY, SIMILARITY_BOOST, eleven_api_key)

if __name__ == "__main__":
    main()
