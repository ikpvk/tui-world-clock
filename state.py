from models import Clock
from config_manager import ConfigManager


class AppState:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()

        self.format_24h = self.config.get("format_24h", True)
        self.clocks = []

        self._load_clocks()

    def _load_clocks(self):
        self.clocks = []

        for item in self.config.get("timezones", []):
            try:
                clock = Clock(label=item["label"], zone=item["zone"])
                self.clocks.append(clock)
            except ValueError:
                continue

    def add_clock(self, label, zone):
        clock = Clock(label=label, zone=zone)
        self.clocks.append(clock)

        self.config["timezones"].append({
            "label": label,
            "zone": zone
        })

        self.config_manager.save(self.config)

    def remove_clock(self, index):
        if 0 <= index < len(self.clocks):
            del self.clocks[index]
            del self.config["timezones"][index]
            self.config_manager.save(self.config)
