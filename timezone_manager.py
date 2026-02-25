from zoneinfo import available_timezones, ZoneInfo, ZoneInfoNotFoundError


class TimezoneManager:
    def __init__(self):
        # Load and sort once
        self._timezones = sorted(available_timezones())

    def list_all(self):
        return self._timezones

    def is_valid(self, zone: str) -> bool:
        try:
            ZoneInfo(zone)
            return True
        except ZoneInfoNotFoundError:
            return False

    def search(self, query: str, limit: int = 20):
        """
        Case-insensitive substring search.
        Returns top `limit` matches.
        """
        if not query:
            return self._timezones[:limit]

        query_lower = query.lower()

        matches = [
            tz for tz in self._timezones
            if query_lower in tz.lower()
        ]

        return matches[:limit]
