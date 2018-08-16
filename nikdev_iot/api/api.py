# -*- coding: utf-8 -*-

import atexit
import time

from nikdev_iot.config import Config
from nikdev_iot.network.network import NetworkStatus
from nikdev_iot.objects import Value, Entry, Batch
from nikdev_iot.network import Network

from .api_exception import ApiException


class _BaseApi(object):

    config = None
    """
    The configuration class for the API. Can be used to access configuration values.
    
    :type: Config
    """

    network = None

    def __init__(self, config=None):
        """
        Initializes the API with a config dictionary.

        :param config:      The given API key needed to connect to the server.
        :type config: dict
        """
        # Store the config locally
        self.config = Config(config)
        self.network = Network(self.config)

    @classmethod
    def from_credentials(cls, device_id, api_key):
        """
        Initializes the API with credentials only and uses the default settings for everything else.

        :param device_id:   The id of the device that the API is trying to connect to.
        :param api_key:     The given API key needed to connect to the server.
        :type device_id: str
        :type api_key: str
        """
        return cls({
            'deviceId': device_id,
            'apiKey': api_key
        })


class _UpstreamApi(_BaseApi):

    values = []
    """
    Stores added values that hasn't been committed yet.
    
    :type: list[object]
    """

    entries = []
    """
    Stores committed entries that hasn't been pushed yet.
    
    :type: list[object]
    """

    def add_value(self, field_id, value):
        """
        Adds a value to be committed and updates it if a value with the field_id already exists.

        :param field_id:    The represented field_id
        :param value:       The value to store.
        :return:            Returns the added Value object.
        :rtype: Value
        """
        # Sets initial variable to check if the value was updated or not
        updated = False
        # Create the value object
        new_value_object = Value(field_id, value)
        # Iterate over all added values
        for idx, old_value_object in enumerate(self.values):
            # Check if the new value has already been set previously.
            if old_value_object == new_value_object:
                # If so, update it instead.
                self.values[idx] = new_value_object
                updated = True

        # Check if we updated the value or not
        if not updated:
            # If we didn't add it to values instead.
            self.values.append(new_value_object)

        return new_value_object

    def reset(self):
        """
        Deletes all uncommitted values.
        """
        self.values = []

    def commit(self):
        # Get the current timestamp
        commit_timestamp = int(time.time())
        # Create a new entry, and pass the values by value (instead of by reference)
        entry = Entry(timestamp=commit_timestamp, values=self.values[:])
        # Add the entry to the entries
        self.entries.append(entry)
        # Delete the committed values
        self.reset()

    def push(self):
        """
        Takes the commited entries and send them to the server.
        """
        client_timestamp = int(time.time())
        batch = Batch(timestamp=client_timestamp, entries=self.entries)

        status, response = self.network.post(
            url=self.config.get_value('baseUrl') + 'entries/',
            json=batch.to_object_upstream()
        )

        if status == NetworkStatus.SUCCESS:
            self.reset_unpushed_entries()
        elif status == NetworkStatus.BAD_REQUEST:
            self.reset_unpushed_entries()
            try:
                error_message = response.json()['message']
            except ValueError:
                error_message = str(response.status_code)
            raise ApiException('Bad request: ' + error_message)
        elif status == NetworkStatus.BAD_LUCK:
            raise ApiException('Bad luck: client timeout or unexpected server error.')

    def reset(self):
        """
        Deletes all uncommitted values.
        """
        self.values = []

    def reset_unpushed_entries(self):
        """
        Deletes all entries that haven't been pushed.
        """
        self.entries = []
        raise NotImplemented


class _DownstreamApi(_UpstreamApi):

    def get(self, field_ids=None):
        raise NotImplemented


class _StorageApi(_DownstreamApi):

    def __init__(self, config=None):
        super(_StorageApi, self).__init__(config)

        if self.config.get_value('stageUncommittedValues', False):
            # Register destructor, to make sure uncommitted values won't be lost
            atexit.register(self._stage_values)
            self._restore_values()

        if self.config.get_value('stageUnpushedEntries', False):
            # Register destructor, to make sure unpushed entries won't be lost
            atexit.register(self._stage_entries)
            self._restore_entries()

    def _stage_values(self, values):
        # TODO: Implement catch to store uncommitted values
        pass

    def _stage_entries(self, entries):
        # TODO: Implement catch to store unpushed entries
        pass

    def _restore_values(self):
        # TODO: Implement function to restore uncommitted values
        pass

    def _restore_entries(self):
        # TODO: Implement function to restore unpushed entries
        pass


class Api(_DownstreamApi):
    pass
