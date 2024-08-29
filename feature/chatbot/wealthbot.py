import nltk
from nltk.tokenize import word_tokenize
import json

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ChatBot:
    def __init__(self, knowledge_base_file='feature/chatbot/knowledge_base.json'):
        self.knowledge_base_file = knowledge_base_file
        try:
            with open(self.knowledge_base_file, 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = {"intents": []}

    def learn_and_respond(self, user_input):
        response = self.find_response(user_input)
        if response is None:
            response = input(f"I don't have a response. Please teach me a response for '{user_input}': ")
            self.teach_response(user_input, response)

        # Save the updated knowledge base to JSON file
        self.save_knowledge_base()

        return response

    def find_response(self, user_input):
        user_input_tokens = word_tokenize(user_input.lower())
        for intent in self.knowledge_base.get('intents', []):
            for example in intent['examples']:
                example_tokens = word_tokenize(example['query'].lower())
                if user_input_tokens == example_tokens:
                    return example['response']
        return None

    def teach_response(self, user_input, response):
        user_intent = input("What intent does this query belong to?: ")
        new_example = {"query": user_input, "response": response}

        # Check if the intent already exists
        for intent in self.knowledge_base.get('intents', []):
            if intent['intent'].lower() == user_intent.lower():
                intent['examples'].append(new_example)
                break
        else:
            # If the intent does not exist, create a new one
            new_intent = {"intent": user_intent, "examples": [new_example]}
            self.knowledge_base['intents'].append(new_intent)

    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=4)

    def chat(self):
        print("Welcome! Let's chat. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                self.save_knowledge_base()
                print("Exiting...")
                break
            else:
                response = self.learn_and_respond(user_input)
                print(f"Bot: {response}")

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.chat()



    #routes pending
