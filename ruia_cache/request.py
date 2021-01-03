#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""

import asyncio

from inspect import iscoroutinefunction

import async_timeout

from ruia import Request, Response

from ruia_cache.cache_patch import req_cache


class RequestCacheSpider(Request):
    """
    Ruia cache request
    Adding caching features to Ruia
    """

    @req_cache
    async def fetch(self, delay=True) -> Response:
        """Fetch all the information by using aiohttp"""
        return await super().fetch(delay)
