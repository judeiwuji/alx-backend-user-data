#!/usr/bin/env python3
"""Module: Filtered Logger"""
from typing import List, Dict


def parse_data(data: str, sep: str) -> Dict[str, str]:
    """parse message into dict"""
    if data is None:
        return {}
    return {d.split('=')[0]: d.split('=')[1] for d in data.split(sep) if d}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """filter datum method"""
    parsed = parse_data(message, separator)
    for field in fields:
        message = message.\
            replace('{}={}'.format(field, parsed[field]),
                    '{}={}'.format(field, redaction))
    return message
