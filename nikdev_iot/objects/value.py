# -*- coding: utf-8 -*-


class Value:

    field_id = None
    """ 
    The field id to store the value to.
    
    :type: str
    """

    value = None
    """
    The actual value that is sent to the server.

    :type: str|int|float|bool
    """

    timestamp = None
    """
    (optional) Timestamp that stores the timestamp when the value was set. 
    Only for read, will not sent on upload or converted with to_object function.
    
    :type: int
    """

    def __init__(self, field_id=None, value=None, timestamp=None, json_data=None):
        """
        Initializes a value object, either for reading or storing on the IoT Server.

        :param str                  field_id:   The field id or json object to serialize from.
        :param str|int|float|bool   value:      (optional) The value of the field.
        :param int                  timestamp:  (optional) The timestamp of the set value.
        :param dict                 json_data:  JSON-data that initialize the object. Can not be set together with other.
        """
        # Check if first argument is field or dict
        if json_data is not None:
            self.field_id = json_data.get('field_id')
            self.value = json_data.get('value')
            self.timestamp = json_data.get('timestamp')
        elif field_id is not None:
            # If dict, proceed to populate the fields
            self.field_id = field_id
            self.value = value
            self.timestamp = timestamp

    def to_object(self):
        """
        Converts the object to a dict that can be sent to the server.

        :return:    A represented dict to store on server.
        :rtype:     object
        """
        return {
            'field_id': self.field_id,
            'value': self.value,
            'timestamp': self.timestamp if self.timestamp is not None else None
        }
