import time

from value import Value

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


        :param timestamp:
        :param values:
        """
        self.timestamp  = timestamp if timestamp    else int(time.time())
        self.values     = values    if values       else []

    def to_object(self):
        """
        Converts the object to a dict that can be sent to the server.

        :return:    A represented dict to store on server.
        :rtype:     dict[int, list[Value]]
        """
        # Serialize all the values before returning the entry.
        _values = []
        for value in self.values:
            _values.append(value.to_object())
        return {'timestamp': self.timestamp, 'values': _values}

    def __getitem__(self, item):
        print 'wow'

    def test(self, wow=None):
