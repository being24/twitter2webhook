import os
import pathlib
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from zoneinfo import ZoneInfo
except ModuleNotFoundError:
    from backports import zoneinfo as ZoneInfo

import tweepy
from dotenv import load_dotenv


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


class FailedToGetResponse(Exception):
    """TwitterAPIからのレスポンスが正常ではないことを知らせる例外クラス"""

    pass


@dataclass
class TweetData:
    name: str
    id: int
    text: str
    profile_image_url: str
    user_name: str
    created_at: datetime | None = None

    def __post_init__(self):
        self.created_at = Snowflake().convert(self.id)


class TwitterUtils:
    def __init__(self) -> None:
        root_path = pathlib.Path(__file__).parents[2]
        dotenv_path = root_path / ".env"

        self.scp_jp_announce_id = 1110524129889779713

        if not dotenv_path.is_file():
            print(dotenv_path)
            raise FileNotFoundError(".env file not found")

        load_dotenv(dotenv_path)

        Bearer_Token = os.getenv("Bearer_Token")
        if Bearer_Token is None:
            raise ValueError("Bearer_Token is None")

        self.client = tweepy.Client(Bearer_Token)

    def get_timeline(self) -> list[TweetData]:
        tweets = self.client.get_users_tweets(id=self.scp_jp_announce_id)
        user = self.client.get_user(id=self.scp_jp_announce_id, user_fields=["profile_image_url"])

        if not isinstance(tweets, tweepy.Response):
            raise FailedToGetResponse

        if not isinstance(user, tweepy.Response):
            raise FailedToGetResponse

        # tweetsをTweetDataのリストにリスト内包表記で変換
        return [
            TweetData(
                name=user.data.name,
                id=tweet.id,
                text=tweet.text,
                profile_image_url=user.data.profile_image_url,
                user_name=user.data.username,
            )
            for tweet in tweets.data
        ]

    def gen_tweet_url(self, screen_name, id):
        return f"https://twitter.com/{screen_name}/status/{id}"


if __name__ == "__main__":
    twitter = TwitterUtils()
    result = twitter.get_timeline()
    print(result)
