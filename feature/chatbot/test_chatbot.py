import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Initialize lemmatizers
lemmatizer = WordNetLemmatizer()

# Define file paths
intents_file = 'data\\test_data_chatbot.json'
words_file = 'words.pkl'
classes_file = 'classes.pkl'
model_file = 'chatbot_model.h5'

# Load the intents file
with open(intents_file, 'r') as file:
    intents = json.load(file)

# Load words, classes, and model
words = pickle.load(open(words_file, 'rb'))
classes = pickle.load(open(classes_file, 'rb'))
model = load_model(model_file)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

import random

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
        if i['intent'] == tag:
            examples = i['examples']
            # Pick a random example's response
            result = random.choice(examples)['response']
            break
    return result


print("GO! Bot is running!")

while True:
    message = input("You: ")

    # Check if the user wants to end the conversation
    if message.lower() in ["bye", "goodbye", "exit", "quit"]:
        print("Bot: Goodbye! Have a great day!")
        break
    ints = predict_class(message)
    if ints:
        res = get_response(ints, intents)
        print(f"Bot: {res}")
    else:
        print("Bot: I'm sorry, I didn't understand that.")
