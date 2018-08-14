# -*- coding: utf-8 -*-

from nikdev_iot.config import Config
import time


class BaseApi:

    config = None
    """
    The configuration class for the API. Can be used to access configuration values.
    
    :type: Config
    """

    def __init__(self, config=None):
        self.config = Config(config)

    def set_credentials(self, device_id, api_key):
        """
        Sets the credentials for the Api.

        :type device_id: str
        :param device_id:   The id of the device that the API is trying to connect to.
        :type api_key: str
        :param api_key:     The given API key needed to connect to the server.
        """
        self.config.set_value('deviceId', device_id)
        self.config.set_value('apiKey', api_key)


class UpstreamApi(BaseApi):

    def add_value(self, field, value):
        pass

    def reset(self):
        pass

    def commit(self):
        commit_timestamp = int(time.time())
        pass

    def push(self):
        client_timestamp = int(time.time())
        pass


class DownstreamApi(BaseApi):

    def get(self, field_ids=None):
        pass

class Api(BaseApi, UpstreamApi, DownstreamApi):
    pass