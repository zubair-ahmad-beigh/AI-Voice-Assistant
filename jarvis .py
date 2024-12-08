import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import requests
import wikipedia
import webbrowser
import pygame
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Set a slower rate of speech
engine.setProperty('rate', 150)

def speak(audio):
    # Reinitialize engine to avoid missed words
    engine = pyttsx3.init('sapi5')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    
    # Add a slight buffer before speaking
    engine.say(" ")
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to take voice input from the user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=10)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak("say that again please...")
        return "none"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning")
    elif hour > 12 and hour <= 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Joy Lobo sir. Please tell me how can I help you")

def get_weather(city):
    api_key = "08e7d9b3249222d81e0abe22fd87e7ca"  # Your valid OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    # Check if the "main" key is in the response
    if "main" in data:
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}. Humidity is {humidity} percent.")
    else:
        error_message = data.get("message", "Sorry, I couldn't find the weather for that location.")
        speak(error_message)

if __name__ == "__main__":
    wish()

    while True:
        query = takecommand().lower()

        if "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "D:\\music"
            songs = os.listdir(music_dir)
            if songs:
                song_path = os.path.join(music_dir, random.choice(songs))  # Play a random song
                pygame.mixer.music.load(song_path)  # Load the selected song
                pygame.mixer.music.play()  # Play the song
            else:
                speak("No music files found in the directory")

        elif "ip address" in query:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "open youtube" in query:
            speak("Sir, what should I search?")
            search_query = takecommand().lower()
            if search_query != "none":
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif "weather" in query:
            speak("Please tell me the city name.")
            city = takecommand().lower()
            if city != "none":
                get_weather(city)
