#!/usr/bin/env python3
"""Module: Filtered Logger"""
from typing import List, Dict
import logging
import re


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """create a new instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a log"""
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        record.msg = filtered
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter datum method"""
    for field in fields:
        message = re.sub(re.compile(field + r'=.+?' + separator),
                         f"{field}={redaction}{separator}", message)
    return message
