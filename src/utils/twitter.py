#!/usr/bin/env python
# coding: utf-8

import json
import os
import pathlib

from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session


class FailedToGetResponse(Exception):
    """TwitterAPIからのレスポンスが正常ではないことを知らせる例外クラス"""
    pass


class TwitterUtils():
    def __init__(self) -> None:
        root_path = pathlib.Path(__file__).parents[2]
        dotenv_path = root_path / '.env'

        if not dotenv_path.is_file():
            print(dotenv_path)
            raise FileNotFoundError(".env file not found")

        load_dotenv(dotenv_path)

        self.CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

        self.KEY = (
            self.CONSUMER_KEY,
            self.CONSUMER_SECRET,
            self.ACCESS_TOKEN,
            self.ACCESS_TOKEN_SECRET
        )

        if any(i is None for i in self.KEY):
            raise ValueError(self.KEY)

    def get_timeline(self) -> dict:
        twitter = OAuth1Session(*self.KEY)

        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        # scpjp_announce
        params = {'screen_name': 'scpjp_announce', 'count': 5}
        res = twitter.get(url, params=params)

        result_dict = {}

        if res.status_code == 200:  # 正常通信出来た場合
            timelines = json.loads(res.text)  # レスポンスからタイムラインリストを取得
            for line in timelines:  # タイムラインリストをループ処理
                # print(f"{root_url}{line['id']}")
                result_dict[line['id']] = {'created_at': line['created_at'],
                                           'name': line['user']['name'],
                                           'avator_url': line['user']['profile_image_url'],
                                           'screen_name': line['user']['screen_name']}
        else:  # 正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            raise FailedToGetResponse

        return result_dict
