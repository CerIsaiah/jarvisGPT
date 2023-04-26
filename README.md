# **🤖 Adam - Your Personal Voice Assistant 🎙️**
Adam is a personal voice assistant that uses speech recognition, text-to-speech, and various APIs to answer your questions and perform online searches. 🌐

## 🚀 Features 
🎤 Listen for voice commands and recognize user input.

🔍 Perform Google searches and return the top results.

💬 Chat with OpenAI GPT-3.5-turbo for natural language understanding and responses.

🎧 Convert text-to-speech using the ElevenLabs API.

🔄 Continuous activation and deactivation with voice commands.

## 🎯 How to Use 
Set up your API keys for OpenAI, Google, and ElevenLabs using the .env.template file. After changing values rename the template to .env

Run the script with python adam.py.

Wait for the "Waiting for activation command..." prompt.

Say "Adam activate" to start interacting with your voice assistant.

Ask questions or give commands like "search online" followed by your query.

To deactivate Adam, say "Exit" or "Power down".

## 📚 Functions  
listen(timeout, phrase_time_limit): Listen for user input using a microphone and returns the recognized text.

elevenlabs_speak(text, voice_id, stability, similarity_boost, ELEVENLABS_API_KEY, volume): Convert the given text to speech using ElevenLabs API and play the audio.

google_search(search_term, api_key, cse_id, **kwargs): Perform a Google search using the given search term and return the search results.

ask_openai(prompt): Ask OpenAI GPT-3.5-turbo a question and return the model's response.

main(): Main function to handle the activation, deactivation, and interaction with the voice assistant.

Happy chatting with Adam, your personal voice assistant! 🤖💬🎉
