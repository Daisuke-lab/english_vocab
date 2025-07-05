from google import genai
import os
import sys
from dotenv import load_dotenv
import re
#https://github.com/google-gemini/gemini-api-quickstart
class GeminiManager:

    def __init__(self):
        curr_dir = self.get_curr_dir()
        load_dotenv(os.path.join(curr_dir, ".env"))
        api_key = os.environ.get("GEMINI_API_KEY")
        print("KEY:", api_key)
        #os.environ["GEMINI_API_KEY"] = api_key
        self.client = genai.Client()
        self.chat = self.client.chats.create(model="gemini-2.5-pro")
        self.init_chat()

    def get_curr_dir(self):
        # Pyinstaller exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        # general python
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path
    
    def init_chat(self):
        curr_dir = self.get_curr_dir()
        path = os.path.join(curr_dir, "first_prompt.txt")
        with open(path) as f:
            prompt = f.read()
        res = self.chat.send_message(prompt)
        print(self.parse_response(res.text))

    def search_word(self, word):
        prompt = f"What is the meaning of {word}?"
        res = self.chat.send_message(prompt)
        return self.parse_response(res.text)

    def parse_response(self, text):
        text = text.strip()

        # Regular expression pattern to match keys and lists of strings
        pattern = r'"(\w+)":\s*\[(.*?)\]'

        matches = re.findall(pattern, text, re.DOTALL)

        output = {}
        for key, list_str in matches:
            # Find all strings inside the brackets
            items = re.findall(r'"(.*?)"', list_str)
            output[key] = items
        return output


if __name__ == "__main__":
    GeminiManager()