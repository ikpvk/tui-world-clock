import json
from pathlib import Path
from platformdirs import user_config_dir


APP_NAME = "tui-world-clock"

DEFAULT_CONFIG = {
    "format_24h": True,
    "timezones": [
        {
            "label": "India",
            "zone": "Asia/Kolkata"
        }
    ]
}


class ConfigManager:
    def __init__(self):
        config_path = user_config_dir(APP_NAME)
        self.config_dir = Path(config_path)
        self.config_file = self.config_dir / "config.json"

        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self._write_default()

    def _write_default(self):
        with open(self.config_file, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    def load(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._write_default()
            return DEFAULT_CONFIG.copy()

    def save(self, config_data: dict):
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=4)
