#!/usr/bin/env python3
'''
    Logger Module
'''
import logging
import mysql.connector
import os
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
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' Returns a connector to the database '''
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    connector = mysql.connector.connection.MySQLConnection(host=host,
                                                           database=db_name,
                                                           user=username,
                                                           password=password)
    return connector


def main():
    ''' obtain a database connection using get_db and retrieve all rows in the
        users table and display each row under a filtered format
    '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    description = [desc[0] for desc in cursor.description]
    logger = get_logger()
    for row in cursor:
        message = "".join([f'{des}={val};'
                          for des, val in zip(description, row)])
        logger.info(message)
    cursor.close()
    db.close()


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
