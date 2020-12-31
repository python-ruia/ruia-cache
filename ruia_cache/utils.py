#!/usr/bin/env python
"""
 Created by howie.hu at 2020/12/31.
"""

import hashlib


def md5_encryption(string: str) -> str:
    """
    MD5 encryption of string
    :param string:
    :return:
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()
