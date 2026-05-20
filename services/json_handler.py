import json
import os

class JsonStorage:
    def __init__(self, filename):
        self.path = os.path.join("storage", filename)
        if not os.path.exists("storage"):
            os.makedirs("storage")

    def save(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []



