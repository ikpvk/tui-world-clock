from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass
class Clock:
    label: str
    zone: str

    def __post_init__(self):
        # Validate timezone immediately
        try:
            ZoneInfo(self.zone)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {self.zone}")

    def _now(self) -> datetime:
        return datetime.now(ZoneInfo(self.zone))

    def get_time(self, format_24h: bool = True) -> str:
        now = self._now()
        if format_24h:
            return now.strftime("%H:%M:%S")
        return now.strftime("%I:%M:%S %p")

    def get_utc_offset(self) -> str:
        now = self._now()
        offset = now.utcoffset()

        if offset is None:
            return "UTC+00:00"

        total_seconds = int(offset.total_seconds())
        sign = "+" if total_seconds >= 0 else "-"
        total_seconds = abs(total_seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return f"UTC{sign}{hours:02d}:{minutes:02d}"
