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
from keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil
import json
import pickle
import subprocess
import sounddevice as sd
import numpy as np
import wave
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator

from main import speak

# Directory to store wake-word dataset
wake_word_dir = "./wake_word_dataset/hey_ram"
background_dir = "./wake_word_dataset/background"

os.makedirs(wake_word_dir, exist_ok=True)
os.makedirs(background_dir, exist_ok=True)

# Parameters
fs = 44100  # Sample rate
duration = 2  # 1 second per sample
num_samples = 100  # Adjust as needed

# def record_audio(filename):
#     print(f"Recording {filename}...")
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
#     sd.wait()
#     wavefile = wave.open(filename, 'wb')
#     wavefile.setnchannels(1)
#     wavefile.setsampwidth(2)
#     wavefile.setframerate(fs)
#     wavefile.writeframes(audio.tobytes())
#     wavefile.close()
#     print(f"Saved: {filename}")

# # Record wake-word samples
# for i in range(num_samples):
#     input(f"Press Enter and say 'Hey Ram' ({i+1}/{num_samples})")
#     record_audio(f"{wake_word_dir}/hey_ram_{i}.wav")

# # Record background noise samples
# for i in range(num_samples):
#     input(f"Press Enter to record background noise ({i+1}/{num_samples})")
#     record_audio(f"{background_dir}/background_{i}.wav")

# print("Dataset collection complete!")
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# import numpy as np
# import os

# def generate_spectrogram(audio_path, output_path):
#     y, sr = librosa.load(audio_path, sr=16000)
#     S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
#     S_dB = librosa.power_to_db(S, ref=np.max)

#     plt.figure(figsize=(4, 4))
#     librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
#     plt.axis('off')
#     plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
#     plt.close()

# # Convert dataset to spectrograms
# for category in ["hey_ram", "background"]:
#     input_folder = f"./wake_word_dataset/{category}"
#     output_folder = f"./spectrograms/{category}"
#     os.makedirs(output_folder, exist_ok=True)

#     for filename in os.listdir(input_folder):
#         if filename.endswith(".wav"):
#             generate_spectrogram(os.path.join(input_folder, filename), os.path.join(output_folder, filename.replace(".wav", ".png")))

# print("Spectrograms generated!")

train_data_dir = "./spectrograms/"
img_size = (64, 64)

datagen = ImageDataGenerator(validation_split=0.2, rescale=1./255)

train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=img_size,
    batch_size=32,
    class_mode='binary',
    subset='training')

val_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=img_size,
    batch_size=32,
    class_mode='binary',
    subset='validation')

# Build CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])
def plot_training_history(history):
    plt.figure(figsize=(12, 5))

    # Plot Loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss', color='blue')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='red')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    # Plot Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy', color='blue')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', color='red')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    plt.show()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.summary()

# Train model
history = model.fit(train_generator, validation_data=val_generator, epochs=10)
# Visualize training and validation metrics
plot_training_history(history)
# Save model
model.save("wake_word_model.h5")
print("Model training complete!")
import sounddevice as sd
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

with open("./intents.json") as file:
    data = json.load(file)

model = load_model("./chat_model.h5")

with open("./tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("./label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

model = tf.keras.models.load_model("wake_word_model.h5")

def predict_wake_word(audio):
    # Convert audio to spectrogram
    S = librosa.feature.melspectrogram(y=audio, sr=16000, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # Resize to match model input
    plt.figure(figsize=(4, 4))
    librosa.display.specshow(S_dB, sr=16000, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.savefig("temp.png", bbox_inches='tight', pad_inches=0)
    plt.close()

    img = cv2.imread("temp.png")
    img = cv2.resize(img, (64, 64)) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    return prediction[0][0] > 0.5  # True if "Hey Ram" detected

def listen_for_wake_word():
    print("Listening for 'Hey Ram'...")
    while True:
        audio = sd.rec(int(1 * 16000), samplerate=16000, channels=1, dtype=np.float32)
        sd.wait()

        if predict_wake_word(audio.flatten()):
            print("Wake word detected!")
            speak("How can I assist you?")
            return True

listen_for_wake_word()
