#!/usr/bin/env python3
'''
    Logger Module
'''
import logging
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password', )


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' Function that returns the log message obfuscated '''
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    ''' Returns a logging.Logger object'''
    logger = logging.getLogger("user_data")
    logger.setLevel(20)
    logger.propagate(False)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        ''' Logging constructor'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' Filters values in incoming log records using filter_datum '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
