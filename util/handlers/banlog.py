import json
import os

__all__ = ["BanLogHandler"]


class BanLogHandler:

    def __init__(self):
        if not os.path.exists("banlog.json"):
            with open("banlog.json", "w") as file:
                file.write("{}")
                file.close()

    data = None

    def load_data(self):
        with open("banlog.json", "r") as file:
            self.data = json.load(file)
            file.close()

    def save_data(self):
        with open("banlog.json", "w") as file:
            json.dump(self.data, file)
            file.close()

    def add_entry(self, bot_id: int, ban_data: dict):
        self.data[bot_id] = ban_data
