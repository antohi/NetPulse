import json

class ConfigManager:
    def __init__(self):
        # Paths for JSON files
        self.score_config_path = "src/score_config.json"
        self.known_devices_config_path = "src/known_devices_config.json"
        self.trusted_vendors_config_path = "src/trusted_vendors_config.json"

    # Loads config path
    def load_json(self, config):
        with open(config, "r") as f:
            return json.load(f)

    # Saves updated config value
    def save_config(self, config, data):
        with open(config, "w") as f:
            json.dump(data, f, indent=2)
