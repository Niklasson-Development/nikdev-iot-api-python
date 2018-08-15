# -*- coding: utf-8 -*-

import time
from . import Value


class Entry:

    values = []
    """
    :type: list[Value]
    """

    timestamp = None
    """
    Store the timestamp when the values was set.
    Only for read, will not sent on upload or converted with to_object function.
    
    :type: int
    """

    def __init__(self, timestamp=None, values=None):
        """
        Creates an Entry object that can store values and timestamp of data to be uploaded.

        :param int timestamp:       The timestamp to be set to the server. If empty, set from the current client time.
        :param list[Value] values:  A list of values to be sent to the server.
        """
        self.timestamp = timestamp if timestamp else int(time.time())
        self.values = values if values else []

    def to_object_downstream(self):
        """
        Converts the object to a dict that represents what was fetched from the server.

        :return:    A represented dict that matches the server structure.
        :rtype:     dict[int, list[Value]]
        """
        # Serialize all the values before returning the entry.
        _values = []
        for value in self.values:
            _values.append(value.to_object_downstream())
        return {'timestamp': self.timestamp, 'values': _values}

    def to_object_upstream(self):
        """
        Converts the object to a dict that can be sent to the server.

        :return:    A represented dict to store on server.
        :rtype:     dict[int, list[Value]]
        """
        # Serialize all the values before returning the entry.
        _values = []
        for value in self.values:
            _values.append(value.to_object_upstream())
        return {'timestamp': self.timestamp, 'values': _values}
