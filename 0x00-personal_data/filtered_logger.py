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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR).\
            replace(";", "; ")
        record.msg = filtered
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """filter datum method"""
    for field in fields:
        pattern = re.compile(field + r'=.+?' + separator)
        message = re.sub(pattern, "{}={}{}".format(
            field, redaction, separator), message,)
    return message
