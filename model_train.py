import json
import pickle
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras_preprocessing.text import Tokenizer #Tokenizer is used to tokenize the text to some kind of token
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder #LabelEncoder is used to encode the labels just to convert the labels into numbers
import matplotlib.pyplot as plt
with open("./intents.json") as file:
    data = json.load(file)
training_sentences = [] #traoning_sentences is used to store the patterns
training_labels = [] #training_labels is used to store the tags
labels=[] #labels is used to store the tags
responses = [] #responses is used to store the responses

for intent in data['intents']: 
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

number_of_classes = len(labels)

print(number_of_classes)

label_encoder =LabelEncoder()
label_encoder.fit(training_labels)
training_labels = label_encoder.transform(training_labels)

vocab_size = 1000
max_len = 20
ovv_token = "<OOV>" #OOV is used to replace the words which are not in the vocabulary
embedding_dim = 16

tokenizer = Tokenizer(num_words=vocab_size, oov_token=ovv_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(number_of_classes, activation="softmax"))

model.compile(loss='sparse_categorical_crossentropy', optimizer="adam", metrics=["accuracy"])

model.summary()

history = model.fit(padded_sequences, np.array(training_labels), epochs = 1000)

# # epochs = 500
# # Visualize errors using Matplotlib after training
# def plot_training_history(history):
#     plt.figure(figsize=(12, 5))

#     # Plot Loss
#     plt.subplot(1, 2, 1)
#     plt.plot(history.history['loss'], label='Training Loss', color='blue')
#     plt.xlabel('Epochs')
#     plt.ylabel('Loss')
#     plt.title('Training Loss Over Epochs')
#     plt.legend()

#     # Plot Accuracy
#     plt.subplot(1, 2, 2)
#     plt.plot(history.history['accuracy'], label='Training Accuracy', color='green')
#     plt.xlabel('Epochs')
#     plt.ylabel('Accuracy')
#     plt.title('Training Accuracy Over Epochs')
#     plt.legend()

#     plt.show()

# # Call the function to visualize training history
# plot_training_history(history)

model.save("chat_model.h5")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

with open("label_encoder.pkl", "wb") as encoder_file:
    pickle.dump(label_encoder, encoder_file, protocol=pickle.HIGHEST_PROTOCOL)
