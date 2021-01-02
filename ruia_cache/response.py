#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/2.
"""
from ruia import Response

from ruia_cache.cache import resp_cache


class CacheResponse(Response):
    """
    Ruia cache response
    """

    spider_name = None
    _source_resp: Response = None

    @resp_cache
    async def json(self, *args, **kwargs):
        """Read and decodes JSON response."""
        return await self._source_resp.json(*args, **kwargs)

    @resp_cache
    async def read(self):
        """Read response payload."""
        return await self._source_resp.read()

    @resp_cache
    async def text(self, *args, **kwargs):
        """Read response payload and decode."""
        return await self._source_resp.text(*args, **kwargs)
