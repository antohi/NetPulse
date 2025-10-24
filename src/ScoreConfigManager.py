import json
import os

class ScoreConfigManager:
    def __init__(self):
        self.score_config_path = "src/score_config.json"

    def load_json(self):
        with open(self.score_config_path, "r") as f:
            return json.load(f)

