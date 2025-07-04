import datetime
import os
import re
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 
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

with open("./intents.json") as file:
    data = json.load(file)

model = load_model("./chat_model.h5")

with open("./tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("./label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)


#This is the initialization of the speech recognition engine of spai5 
def initialize_engine():
    engine = pyttsx3.init("sapi5")#sapi5 has the male voice as well as female voice
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate-50) 
    volume = engine.getProperty("volume")
    engine.setProperty("volume", volume+0.25) 
    return engine  

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

#this def command() require internet connection as we are using recognize_google() function It sends the recorded audio to Google's speech recognition API, which processes the audio and returns the recognized text.


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
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 2
    day_dict = {
        1 : "sunday",
        2 : "monday",
        3 : "Tuesday",
        4 : "Wednesday",
        5 : "Thursday",
        6 :  "Friday",
        7 :  "saturday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def WishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()
    
    if(hour>= 0) and (hour<=12) and ('AM' in t):
        speak(f"Good Morning , it's {day} and the time is {t}")
    elif(hour>12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon, it's {day} and time is {t}")
    else:
        speak(f"Good evening, it's {day} and time is {t}")

# def social_media(command):
#     if 'facebook' in command:
#         speak("opening your facebook")
#         webbrowser.open("https://www.facebook.com/")
#     elif 'discord' in command:
#         speak("Opening your discord server")
#         webbrowser.open("https://www.discord.com/")
#     elif 'instagram' in command:
#         speak("Opening your instagram")
#         webbrowser.open("https://www.instagram.com/")
#     elif 'whatsapp' in command:
#         speak("Opening your whatsapp")
#         webbrowser.open("https://www.whatsapp.com/")
#     else:
#         speak("No result")

# def adjust_volume(command):
#     # Regular expression to find the number after "by" in the sentence
#     match = re.search(r'(\d+)', command)
#     if match:
#         volume_change = int(match.group(1))
#     else:
#         volume_change = 1  # Default to 1 if no number is found

#     if "increase the volume by" in command or "raise the volume by" in command:
#         for _ in range(volume_change):
#             pyautogui.press("volumeup")
#         speak(f"Volume increased by {volume_change} level(s)")

#     elif "decrease the volume by" in command or "lower the volume by" in command:
#         for _ in range(volume_change):
#             pyautogui.press("volumedown")
#         speak(f"Volume decreased by {volume_change} level(s)")

#     elif "mute the sound" in command or "volume mute" in command:
#         pyautogui.press("volumemute")
#         speak("Volume muted")
        
# def openApp(command):
#     if "calculator" in command:
#         speak("opening calculator")
#         os.startfile('C:\\Windows\\System32\\calc.exe')
#     elif "notepad" in command:
#         speak("opening notepad")
#         os.startfile('C:\\Windows\\System32\\notepad.exe')
#     elif "paint" in command:
#         speak("opening paint")
#         os.startfile('C:\\Windows\\System32\\mspaint.exe')

# def closeApp(command):
#     if "calculator" in command:
#         speak("closing calculator")
#         os.system("taskkill /f /im calc.exe")
#     elif "notepad" in command:
#         speak("closing notepad")
#         os.system('taskkill /f /im notepad.exe')
#     elif "paint" in command:
#         speak("closing paint")
#         os.system('taskkill /f /im mspaint.exe')
# def browsing(command_text):
#     if 'google' in command_text:
#         speak("Opening google")
#         webbrowser.open("https://www.google.com/")
#         # search_query = command().lower()  # Listen for the search query
#         # search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
#         # webbrowser.open(search_url)  # Open Google search with the query
#         # speak(f"Searching for {search_query}")
#         # webbrowser.open(f"{s}")
#     elif "edge" in command:
#         speak("Opening edge")
#         os.startfile()


# if __name__ == "__main__" :
#     WishMe()
#     while True:
#         # 
#         query = command().lower()
#         # query = input("Enter your command->") 
#         if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
#             social_media(query)
#         elif ("increase the volume by" in query) or ("decrease the volume by" in query):
#             adjust_volume(query)
#         elif ("volume up " in query) or ("increase volume" in query):
#             pyautogui.press("volumeup")
#             speak("Volume increased")
#         elif ("volume down" in query) or ("decrease volume" in query):
#             pyautogui.press("volumedown")
#             speak("Volume decreased")
#         elif ("volume mute" in query) or ("mute the sound" in query):
#             pyautogui.press("volumemute")
#             speak("Volume muted")
#         elif ("opening calculator" in query) or ("open notepad" in query) or ("open paint" in query):
#             openApp(query)
#         elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
#             closeApp(query)
#         elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query) or ("jokes" in query):
#                 padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
#                 result = model.predict(padded_sequences)
#                 tag = label_encoder.inverse_transform([np.argmax(result)])    
                
                
#                 for i in data['intents']:
#                     if i['tag'] == tag:
#                         speak(np.random.choice(i['responses']))
#         elif ("open google" in query) or ("open edge" in query):
#             browsing(query) 
    
#         elif "exit" in query:
#             speak("Goodbye, have a nice day")
#             sys.exit()
            
        # print(query)
        
        
    
# speak("Hello, I am your assistant sujane. How can I help you?")
