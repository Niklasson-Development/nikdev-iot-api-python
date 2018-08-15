# -*- coding: utf-8 -*-

import time
import atexit
from nikdev_iot.config import Config


class BaseApi(object):

    config = None
    """
    The configuration class for the API. Can be used to access configuration values.
    
    :type: Config
    """

    def __init__(self, config=None):
        # Store the config locally
        self.config = Config(config)

    def set_credentials(self, device_id, api_key):
        """
        Sets the credentials for the API calls.

        :param device_id:   The id of the device that the API is trying to connect to.
        :param api_key:     The given API key needed to connect to the server.
        :type device_id: str
        :type api_key: str
        """
        self.config.set_value('deviceId', device_id)
        self.config.set_value('apiKey', api_key)


class UpstreamApi(BaseApi):

    added_values = []

    def __init__(self, config=None):
        super(UpstreamApi, self).__init__(config)

        self.added_values = []

        # Restore previously uncommited values.
        self.__restore_values__()
        # Register destructor, to make sure uncommited values won't be lost
        atexit.register(self.__destruct_upstream__)

    def __destruct_upstream__(self):
        # TODO: Implement catch to store uncommited values
        pass

    def __restore_values__(self):
        pass

    def add_value(self, field, value):
        raise NotImplemented

    def reset(self):
        raise NotImplemented

    def commit(self):
        commit_timestamp = int(time.time())
        raise NotImplemented

    def push(self):
        client_timestamp = int(time.time())
        raise NotImplemented


class DownstreamApi(UpstreamApi):

    def get(self, field_ids=None):
        raise NotImplemented


class Api(DownstreamApi):
    pass
