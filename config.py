import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

CONFIG_FILE = "wormgpt_config.json"

DEFAULT_CONFIG = {
    "api_key": os.getenv("OPENROUTER_API_KEY", ""),
    "base_url": os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1"
    ),
    "model": os.getenv(
        "OPENROUTER_MODEL",
        "tencent/hy3-preview:free"
    ),
    "language": os.getenv(
        "LANGUAGE",
        "English"
    )
}


def load_config():
    # Start with env defaults
    config = DEFAULT_CONFIG.copy()

    # Override with saved config if exists
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved_config = json.load(f)

            # Merge configs
            config.update(saved_config)

        except Exception as e:
            print(f"Config load error: {e}")

    return config


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    return config