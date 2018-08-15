# -*- coding: utf-8 -*-

import requests


class Network:

    _headers = {}

    def __init__(self, config=None):
        """


        :param dict config: The configuration settings for the Api call.
        """
        self._headers = {
            'x-device': config.get('deviceId'),
            'x-api-key': config.get('apiKey')
        }

    @classmethod
    def from_credentials(cls, device_id, api_key):
        return cls({
            'deviceId': device_id,
            'apiKey': api_key
        })

    def post(self, url, json_data):
        return requests.post(url=url, json=json_data, headers=self._headers)

    def get(self, url):
        return requests.get(url=url, headers=self._headers)