# -*- coding: utf-8 -*-


class ApiException(Exception):
    def __init__(self, message):
        super(ApiException, self).__init__(message)
