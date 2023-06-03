import logging
import os
import pathlib
import time

import requests
from dotenv import load_dotenv


class Webhook:
    """
    Webhookを扱うclass
    """

    def __init__(self) -> None:
        root_path = pathlib.Path(__file__).parents[2]
        dotenv_path = root_path / ".env"

        if not dotenv_path.is_file():
            print(dotenv_path)
            raise FileNotFoundError(".env file not found")

        load_dotenv(dotenv_path)

        WEBHOOK_URL = os.getenv("WEBHOOK_URL")

        if WEBHOOK_URL is None:
            raise ValueError("WEBHOOK_URL is None")

        self.USERNAME = "default"
        self.AVATAR_URL = "https://raw.githubusercontent.com/being24/twitter2webhook/master/data/SCPJP.png"
        self.WEBHOOK_URL = WEBHOOK_URL

    def set_parameter(self, username, avatar_url):
        self.USERNAME = username
        self.AVATAR_URL = avatar_url

    def gen_webhook_msg(self, content):
        msg = {"username": self.USERNAME, "avatar_url": self.AVATAR_URL, "content": content}
        return msg

    def send_webhook(self, msg):
        msg = msg or None

        if msg is None or "":
            logging.error("can't send blank msg")
            return -1

        if len(msg) >= 2000:
            logging.error("msg too long!")
            logging.error(msg)
            return -1

        main_content = self.gen_webhook_msg(msg)

        while True:
            response = requests.post(self.WEBHOOK_URL, main_content)
            if response.status_code == 204:
                break
            else:
                err_data = response.json()
                retry_after = int(err_data["retry_after"]) / 1000 + 0.1
                logging.error(response.text)
                logging.error(main_content)
                time.sleep(retry_after)

        time.sleep(0.5)

    def send_webhook_with_embed(self, embed):

        pass


if __name__ == "__main__":
    Webhook().send_webhook("test")
