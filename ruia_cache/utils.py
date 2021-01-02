#!/usr/bin/env python
"""
 Created by howie.hu at 2020/12/31.
 Ruia cache plugin tool module, The following is a description of some environment variables:
    - RUIA_CACHE: cache dir, default value is os.environ["HOME"], status: ok
    - RUIA_CACHE_TTL: Cache expiration time, defaulte value is 86400 ms = 1 day, status: under development
"""
import hashlib
import os

from ruia.utils.log import get_logger

logger = get_logger()


def md5_encryption(string: str) -> str:
    """
    MD5 encryption of string
    :param string:
    :return:
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


def create_cache_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logger.info(f"<Cache dir generated successfully: {path}>")

        logger.info(f"<Cache dir status is ok: {path}>")
    except:
        logger.error(f"<Cache dir gen failed!: {path}>")
    return path


def gen_cache_dir(ruia_cache_path: str = None):
    """
    Generate cache directory for Ruia
    :return:
    """
    ruia_cache_path = ruia_cache_path or os.getenv("RUIA_CACHE", os.environ["HOME"])
    cache_path = os.path.join(ruia_cache_path, ".ruia_cache")
    return create_cache_dir(cache_path)
