import json
import os

import requests


class Chatbot:
    def __init__(self, cache_path: str):
        self.cache_path = cache_path

        self.cache: dict[str, str] = {}

        server = os.getenv("OPEN_WEB_UI_SERVER")
        if server is None:
            raise ValueError("OPEN_WEB_UI_SERVER is not set")
        self.url = f"{server}/api/chat/completions"
        key = os.getenv("OPEN_WEB_UI_API_KEY")
        if key is None:
            raise ValueError("OPEN_WEB_UI_API_KEY is not set")
        self.key = key

        self.load_cache()

    def ask_question(self, question):    
        if question in self.cache:
            return self.cache[question]

        return self.ask_question_without_cache(question)

    def ask_question_without_cache(self, question):
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "llama3.2:latest",
            "messages": [{"role": "user", "content": question}],
        }

        response = requests.post(self.url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code} - {response.text}")
        
        self.cache[question] = response.json()["choices"][0]["message"]["content"]

        # Save cache to file every 10 questions
        if len(self.cache) % 10 == 0:
            print("10 questions asked, saving cache to file")
            self.save_cache()

        return self.cache[question]

    def save_cache(self):
        with open(self.cache_path, "w") as file:
            file.write(json.dumps(self.cache))

    def load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as file:
                self.cache = json.load(file)
