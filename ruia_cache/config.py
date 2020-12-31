#!/usr/bin/env python
"""
 Created by howie.hu at 2020/12/31.
"""
import os

from ruia.utils.log import get_logger

logger = get_logger()


def gen_cache_dir():
    """
    Generate cache directory for Ruia
    :return:
    """
    cache_path = os.path.join(
        os.getenv("RUIA_CACHE", os.environ["HOME"]), ".ruia_cache"
    )

    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
        logger.info(f"<Cache dir generated successfully: {cache_path}>")
    else:
        logger.info(f"<Cache dir already exists: {cache_path}>")
    return cache_path


cache_path = gen_cache_dir()
