import json
import os

CONFIG_FILE = "wormgpt_config.json"
DEFAULT_CONFIG = {
    "api_key": "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",
    "base_url": "https://openrouter.ai/api/v1",
    "model": "deepseek/deepseek-r1-0528:free",
    "language": "English"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Ensure all keys exist
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    return config
