from datetime import datetime
from zoneinfo import ZoneInfo


class Snowflake:
    def __init__(self):
        self.tz = ZoneInfo("Asia/Tokyo")

    def convert(self, snowflake: int) -> datetime:
        """convert snowflake to datetime in JST

        Args:
            snowflake (int): snowflake

        Returns:
            datetime: datetime
        """
        timestamp = ((snowflake >> 22) + 1288834974657) / 1000
        return datetime.fromtimestamp(timestamp, tz=self.tz)


if __name__ == "__main__":
    snowflake = Snowflake()
    id = 1664934961374433282
    print(snowflake.convert(id))
