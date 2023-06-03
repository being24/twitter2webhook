import json
import os
import pathlib
from datetime import datetime

# from utils.webhook import Webhook
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv

from utils.twitter import TwitterUtils


def dump_json(json_path, data) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    root_path = pathlib.Path(__file__).parents[1]
    json_path = root_path / "data" / "setting.json"
    env_path = root_path / ".env"

    load_dotenv(env_path)

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if WEBHOOK_URL is None:
        raise ValueError("WEBHOOK_URL is None")

    tw = TwitterUtils()
    # hook = Webhook()

    last_id = 0000000000000000000

    if not json_path.is_file():
        setting_dict = {}
    else:
        with open(json_path, encoding="utf-8") as f:
            setting_dict = json.load(f)
        last_id = setting_dict["last_id"]

    last_id = 00000000000

    timeline = tw.get_timeline()

    id_list = [i.id for i in timeline]

    index = len(id_list) + 1
    if last_id in id_list:
        index = id_list.index(last_id)
    timeline = timeline[:index]

    if len(timeline) == 0:
        exit()

    webhook = DiscordWebhook(
        url=WEBHOOK_URL,
        username="SCP財団Wiki 日本語版 公式twitter",
        avatar_url=timeline[-1].profile_image_url,
        rate_limit_retry=True,
    )

    for tweet in reversed(timeline):
        url = tw.gen_tweet_url("scp_jp_announce", tweet.id)
        if tweet.created_at is None:
            tweet.created_at = datetime.now()

        embed = DiscordEmbed(
            description=tweet.text,
            color="03b2f8",
        )

        embed.set_author(name=f"{tweet.name}@({tweet.user_name})", url=url, icon_url=tweet.profile_image_url)
        embed.set_timestamp(
            timestamp=tweet.created_at.timestamp()
        )  # TODO: discord-webhookが1.1.0よりバージョンが上がったらdatetimeを渡せるようになるはずなのでそのときはdatetimeを渡すようにする
        webhook.add_embed(embed)

        try:
            response = webhook.execute()
        except Exception as e:
            print(e)

        last_id = tweet.id

    setting_dict["last_id"] = last_id
    dump_json(json_path, setting_dict)
