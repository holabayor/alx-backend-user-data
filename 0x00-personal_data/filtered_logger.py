#!/usr/bin/env python3
'''
    Logger script
'''
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' Function that returns the log message obfuscated '''
    for field in fields:
        log_message = re.sub(f'{field}=.*?{separator}',
                             f'{field}={redaction}{separator}', message)
    return log_message
