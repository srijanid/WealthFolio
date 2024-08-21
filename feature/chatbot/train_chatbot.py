import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define file paths
intents_file = 'data\\test_data_chatbot.json'  

# Initialize lists
documents = []
classes = []
words = []
ignore_letters = ['?', '!', '.', ',']

try:
    # Load intents file
    with open(intents_file, 'r') as file:
        intents = json.load(file)
        
        # Process each intent
        for intent in intents['intents']:
            for example in intent['examples']:
                query = example['query']
                # Tokenize the query
                word_list = nltk.word_tokenize(query)
                words.extend(word_list)
                documents.append((word_list, intent['intent']))
                if intent['intent'] not in classes:
                    classes.append(intent['intent'])

        # Lemmatize and remove duplicates
        words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
        words = sorted(set(words))
        classes = sorted(set(classes))

        # Save words and classes to pickle files
        with open('words.pkl', 'wb') as file:
            pickle.dump(words, file)
        with open('classes.pkl', 'wb') as file:
            pickle.dump(classes, file)

        # Prepare training data
        training = []
        output_empty = [0] * len(classes)

        for document in documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(document[1])] = 1
            training.append(bag + output_row)

        random.shuffle(training)
        training = np.array(training)

        # Split into features and labels
        train_x = training[:, :len(words)]
        train_y = training[:, len(words):]

        # Build the model
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Dense(len(train_y[0]), activation='softmax'))

        # Compile the model
        sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # Train the model
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

        # Save the model
        model.save('chatbot_model.h5')
        print('Model training complete and saved as chatbot_model.h5')

except FileNotFoundError:
    print(f"The file at {intents_file} was not found.")
except json.JSONDecodeError:
    print("Error decoding JSON.")
except Exception as e:
    print(f"An error occurred: {e}")
