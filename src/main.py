#!/usr/bin/env python
# coding: utf-8

import json
import pathlib

from utils.twitter import TwitterUtils
from utils.webhook import Webhook


def dump_json(json_path, data) -> None:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False)


if __name__ == "__main__":
    root_path = pathlib.Path(__file__).parents[1]
    data_path = root_path / 'data'
    json_path = data_path / 'setting.json'

    last_id = 0000000000000000000

    if not json_path.is_file():
        setting_dict = {}
    else:
        with open(json_path, encoding='utf-8') as f:
            setting_dict = json.load(f)
        last_id = setting_dict['last_id']

    tw = TwitterUtils()
    hook = Webhook()

    def gen_tweet_url(screen_name, id):
        return f'https://twitter.com/{screen_name}/status/{id}'

    result_dict = tw.get_timeline()

    id_list = [i for i in result_dict.keys()]

    index = 100
    if last_id in id_list:
        index = id_list.index(last_id)
    result_dict = {k: result_dict[k] for k in list(result_dict)[:index]}

    for id, val in reversed(result_dict.items()):
        hook.set_parameter(username=val['name'], avatar_url=val['avator_url'])
        url = gen_tweet_url(val['screen_name'], id)
        hook.send_webhook(f"{url}\ntweeted at {val['created_at']}")
        last_id = id

    setting_dict['last_id'] = last_id
    dump_json(json_path, setting_dict)
