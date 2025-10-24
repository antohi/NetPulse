import json
import os

class ScoreConfigManager:
    def __init__(self):
        self.score_config_path = "src/score_config.json"

    # Loads config path
    def load_json(self):
        with open(self.score_config_path, "r") as f:
            return json.load(f)

    # Saves updated config value
    def save_config(self, data):
        with open(self.score_config_path, "w") as f:
            json.dump(data, f, indent=2)
        print("[SUCCESS] Updated scoring configuration.")