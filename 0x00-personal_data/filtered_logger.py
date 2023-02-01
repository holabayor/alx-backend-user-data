#!/usr/bin/env python3
'''
    Logger script
'''
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    ''' Function that returns the log message obfuscated
    '''
    for field in fields:
        log_message = re.sub(rf"{field}=(.*?)\{separator}",
                        f'{field}={redaction}{separator}', message)
    return log_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
