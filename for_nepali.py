import datetime
import os
import re
import sys
import threading
import time
import webbrowser
from bs4 import BeautifulSoup
from gtts import gTTS
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil
import json
import pickle
import subprocess
import sounddevice as sd
import librosa
import librosa.display
import cv2
import matplotlib.pyplot as plt
from requests import get
# import food_order
# import food_order
from main import WishMe
import wikipedia
import webbrowser
import smtplib
from pywikihow import search_wikihow,WikiHow
import wolframalpha
import bhojdeals
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from read_news import setopati
import read_news





# Load trained wake-word detection model
wake_word_model = tf.keras.models.load_model("wake_word_model.h5")
# Load assistant AI model
with open("./intents.json") as file:
    data = json.load(file)

model = load_model("./chat_model.h5")

with open("./tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("./label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

engine = pyttsx3.init("sapi5")
# Initialize Text-to-Speech Engine
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

#################################################################################

# Speech Recognition Function
# def command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source, duration=0.5)
#         print("Listening for command...")
#         audio = r.listen(source)
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User said: {query}")
#     except Exception:
#         print("Say that again please...")
#         return "None"
#     return query.lower()

#from main

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5) #handling the noise coming from our microphone
        print("Listening......", end="",flush=True)
        r.pause_threshold = 1 #pause threshold is the time  for which the recognizer will wait for the user to speak before it stops listening
        r.phrase_threshold = 0.3 #phrase threshold is the minimum length of the phrase that the recognizer will accept(it is hit and trial)
        r.sample_rate = 48000 #sample rate is the number of samples of audio carried per second, measured in Hz or kHz
        r.dynamic_energy_threshold = True #dynamic energy threshold is the energy level of the audio above which the recognizer will consider it as speech
        r.operation_timeout = 5 #operation timeout is the time for which the recognizer will wait for the user to speak before it stops listening
        r.non_speaking_duration = 0.5 #non speaking duration is the time for which the recognizer will wait for the user to speak before it stops listening
        r.dynamic_energy_adjustment = 2.5 #dynamic energy adjustment is the factor by which the recognizer will adjust the energy threshold
        r.energy_threshold = 4000 #energy threshold is the energy level of the audio above which the recognizer will consider it as speech
        r.phrase_time_limit = 10 
        # print(sr.Microphone.list_microphone_names()) # it gives the list of microphones connected to the device
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please......")
        return "None"
    return query.lower()


# Wake-word detection function
def predict_wake_word(audio):
    S = librosa.feature.melspectrogram(y=audio, sr=16000, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    plt.figure(figsize=(4, 4))
    librosa.display.specshow(S_dB, sr=16000, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.savefig("temp.png", bbox_inches='tight', pad_inches=0)
    plt.close()

    img = cv2.imread("temp.png")
    img = cv2.resize(img, (64, 64)) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = wake_word_model.predict(img)
    return prediction[0][0] > 0.5  # True if "Hey Ram" detected

# Continuous listening for "Hey Ram"
def listen_for_wake_word():
    print("Listening for wake word 'Hey Ram'...")
    while True:
        audio = sd.rec(int(1 * 16000), samplerate=16000, channels=1, dtype=np.float32)
        sd.wait()

        if predict_wake_word(audio.flatten()):
            print("Wake word detected!")
            speak("How can I assist you?")
            return True
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("sajanoli69@gmail.com","mqcc fsne nhdz ysqe")
    server.sendmail("sajanoli69@gmail.com", to, content)
    server.close()
# Assistant Commands
def social_media(command):
    sites = {
        "facebook": "https://www.facebook.com/",
        "discord": "https://www.discord.com/",
        "instagram": "https://www.instagram.com/",
        "whatsapp": "https://www.whatsapp.com/"
    }
    for site in sites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(sites[site])
            return
    speak("No result")
def adjust_volume(command):
    match = re.search(r'(\d+)', command)
    volume_change = int(match.group(1)) if match else 1

    if "increase" in command or "raise" in command:
        for _ in range(volume_change):
            pyautogui.press("volumeup")
        speak(f"Volume increased by {volume_change} levels")

    elif "decrease" in command or "lower" in command:
        for _ in range(volume_change):
            pyautogui.press("volumedown")
        speak(f"Volume decreased by {volume_change} levels")

    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("Volume muted")

def openApp(command):
    apps = {
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "paint": "C:\\Windows\\System32\\mspaint.exe",
        "media" : "C:\\Windows\\System32\\wmplayer.exe"
    }
    for app in apps:
        if app in command:
            speak(f"Opening {app}")
            os.startfile(apps[app])
            return

def closeApp(command):
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "player" : 'wmplayer.exe'
    }
    for app in apps:
        if app in command:
            speak(f"Closing {app}")
            os.system(f"taskkill /f /im {apps[app]}")
            return

def browsing(command_text):
    if 'google' in command_text:
        speak("Opening Google")
        speak("what do you want to search?")
        search_query = command().lower()
        speak(f"Searching for {search_query}")
        webbrowser.open(search_query)
    elif "youtube" in command_text:
        speak("Opening youtube")
        speak("what do you want to search?")
        search_query = command().lower()
        speak(f"Searching for {search_query}")
        webbrowser.open("https://www.youtube.com/")

# Open and type in CMD
def open_cmd():
    speak("Opening Command Prompt")
    os.system("start cmd")
def execute_pressing_command(command_text):
    if "scroll up" in command_text:
        pyautogui.scroll(7)
        speak("Scrolled up")
    elif "scroll down" in command_text:
        pyautogui.scroll(-10)
        speak("Scrolled down")
    elif "scroll left" in command_text:
        pyautogui.hscroll(3)
        speak("Scrolled left")
    elif "scroll right" in command_text:
        pyautogui.hscroll(-3)
        speak("Scrolled right")
    elif "go back" in command_text or "back" in command_text:
        pyautogui.press("backspace")
        speak("Going back")
    else:
        speak("Command not recognized for pressing control")
        
def execute_browser_command(command_text):
    # Switch to the next tab
    if "switch tab" in command_text or "next tab" in command_text:
        pyautogui.hotkey('ctrl', 'tab')
        speak("Switched to the next tab")
    
    # Switch to the previous tab
    elif "previous tab" in command_text:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        speak("Switched to the previous tab")
    
    # Close the current tab
    elif "close tab" in command_text or "close this tab" in command_text:
        pyautogui.hotkey('ctrl', 'w')
        speak("Closed the current tab")
    
    # Open a new tab
    elif "new tab" in command_text or "open a new tab" in command_text:
        pyautogui.hotkey('ctrl', 't')
        speak("Opened a new tab")
    
    # Open a private (incognito) tab
    elif "private tab" in command_text or "incognito mode" in command_text:
        pyautogui.hotkey('ctrl', 'shift', 'n')
        speak("Opened a private tab")
    
    else:
        speak("Command not recognized for browser control")
# Main Function with Wake-Word Integration
if __name__ == "__main__":
    WishMe()
    while True:
        if listen_for_wake_word():  # Wait until "Hey Ram" is detected
            query = command().lower()
            if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
                social_media(query)
            elif any (word in query for word in ["scroll up", "scroll down", "scroll left", "scroll right", "go back", "back "]):
                execute_pressing_command(query)
            elif any(word in query for word in ["switch tab", "next tab", "previous tab", "close tab", "new tab", "private tab", "incognito mode"]):
                execute_browser_command(query)
            elif ("increase volume" in query) or ("decrease volume" in query):
                adjust_volume(query)
            elif ("mute volume" in query) or ("mute the sound" in query):
                pyautogui.press("volumemute")
                speak("Volume muted")
            elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
                openApp(query)
            elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query) or ("close cmd" in query) or ("stop the player" in query) or ("player" in query):
                closeApp(query)
            elif "open command prompt" in query or "open cmd" in query:
                open_cmd()
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")
            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)  
            elif "send email" in query:
                try:
                    speak("What should I say?")
                    content = command().lower()
                    speak("To whom we should sent the email?")
                    to = command().lower().replace(" ","") + "@gmail.com"
                    print(to)
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry my friend. I am not able to send this email")
            # elif any(word in query for word in ["what", "who", "how", "hi", "hello", "thanks", "joke"]):
            #     padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            #     result = model.predict(padded_sequences)
            #     tag = label_encoder.inverse_transform([np.argmax(result)])

            #     for i in data['intents']:
            #         if i['tag'] == tag:
            #             speak(random.choice(i['responses']))
            elif ("open google" in query) or ("open youtube" in query):
                browsing(query)
            elif "news" in query:
                    speak("Would you like me to read the news for you?")
                    confirmation = command().lower()  # Wait for user to confirm
                    if ("yes read the news" in confirmation) or ("read" in confirmation) or ("news" in confirmation):
                       read_news.setopati()  # Now it will only read news if the user says "yes"
                    else:
                         speak("Okay, I won't read the news.")
            elif 'type' in query:
                query = query.replace("type","")
                pyautogui.typewrite(f"{query}", 0.1)
            elif "calculate" in query:
                app_id = "48GLKT-5EQJ46A4JA"
                client =  wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                query = query.split()[ind + 1:]
                res = client.query(" ".join(query))
                answer = next(res.results).text
                speak("The answer is " + answer)
            elif "what is" in query  or "who is" in query:
                app_id = "48GLKT-5EQJ46A4JA"
                client =  wolframalpha.Client(app_id)
                ind = query.lower().split().index("is")
                query = query.split()[ind + 1:]
                res = client.query(" ".join(query))
                answer = next(res.results).text
                speak("The answer is " + answer)
            elif "where is" in query:
                ind = query.lower().split().index("is")
                location = query.split()[ind + 1:]
                url = "https://www.google.com/maps/place/" + "".join(location)
                speak("This is where "+ str(location) + " is.")
                webbrowser.open(url)
            elif "order food" in query:
                bhojdeals.pizza()
                # food_order.pizza()
            elif "exit" in query:
                speak("Goodbye, have a nice day")
                sys.exit()

########################################################

# import datetime
# import json
# import os
# import pickle
# import re
# import sys
# import time
# import webbrowser
# import pyautogui
# import pyttsx3
# import speech_recognition as sr
# import tensorflow as tf
# from tensorflow import keras
# from keras.models import load_model
# from keras_preprocessing.sequence import pad_sequences
# import numpy as np
# import sounddevice as sd
# import librosa
# import cv2
# import requests
# from requests import get
# import wikipedia
# import smtplib
# import wolframalpha
# import subprocess

# # Suppress TensorFlow warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # Load trained wake-word detection model
# wake_word_model = tf.keras.models.load_model("wake_word_model.h5")

# # Load assistant AI model
# with open("./intents.json") as file:
#     data = json.load(file)

# model = load_model("./chat_model.h5")

# with open("./tokenizer.pkl", "rb") as f:
#     tokenizer = pickle.load(f)

# with open("./label_encoder.pkl", "rb") as encoder_file:
#     label_encoder = pickle.load(encoder_file)

# # Initialize Text-to-Speech Engine
# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[1].id)
# engine.setProperty("rate", 150)
# engine.setProperty("volume", 1.0)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Speech Recognition Function
# def command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User said: {query}")
#     except Exception as e:
#         print("Say that again please...")
#         return "None"
#     return query.lower()

# # Wake-word detection function
# def predict_wake_word(audio):
#     S = librosa.feature.melspectrogram(y=audio, sr=16000, n_mels=128)
#     S_dB = librosa.power_to_db(S, ref=np.max)
#     S_dB = cv2.resize(S_dB, (64, 64)) / 255.0
#     S_dB = np.expand_dims(S_dB, axis=0)
#     prediction = wake_word_model.predict(S_dB)
#     return prediction[0][0] > 0.5  # True if "Hey Ram" detected

# # Continuous listening for "Hey Ram"
# def listen_for_wake_word():
#     print("Listening for wake word 'Hey Ram'...")
#     while True:
#         audio = sd.rec(int(1 * 16000), samplerate=16000, channels=1, dtype=np.float32)
#         sd.wait()
#         if predict_wake_word(audio.flatten()):
#             print("Wake word detected!")
#             speak("How can I assist you?")
#             return True

# # Email Function
# def sendEmail(to, content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login("sajanoli69@gmail.com", "mqcc fsne nhdz ysqe")
#     server.sendmail("sajanoli69@gmail.com", to, content)
#     server.close()

# # Main Function
# if __name__ == "__main__":
#     speak("Hello, I am your voice assistant.")
#     while True:
#         if listen_for_wake_word():  # Wait until "Hey Ram" is detected
#             query = command().lower()

#             if "wikipedia" in query:
#                 speak("Searching Wikipedia...")
#                 query = query.replace("wikipedia", "")
#                 results = wikipedia.summary(query, sentences=2)
#                 speak("According to Wikipedia")
#                 speak(results)

#             elif "open google" in query:
#                 speak("Opening Google")
#                 webbrowser.open("https://www.google.com")

#             elif "open youtube" in query:
#                 speak("Opening YouTube")
#                 webbrowser.open("https://www.youtube.com")

#             elif "send email" in query:
#                 try:
#                     speak("What should I say?")
#                     content = command()
#                     speak("To whom should I send the email?")
#                     to = command().replace(" ", "") + "@gmail.com"
#                     sendEmail(to, content)
#                     speak("Email has been sent!")
#                 except Exception as e:
#                     print(e)
#                     speak("Sorry, I was unable to send the email.")

#             elif "exit" in query:
#                 speak("Goodbye, have a nice day!")
#                 sys.exit()

#             else:
#                 speak("Sorry, I didn't understand that command.")