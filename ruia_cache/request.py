#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""

import asyncio

from inspect import iscoroutinefunction

import async_timeout

from ruia import Request, Response

from ruia_cache.cache import request_cache


class RequestCacheSpider(Request):
    """
    Ruia cache request
    Adding caching features to Ruia
    """

    @request_cache
    async def fetch(self, delay=True) -> Response:
        """Fetch all the information by using aiohttp"""
        if delay and self.request_config.get("DELAY", 0) > 0:
            await asyncio.sleep(self.request_config["DELAY"])

        timeout = self.request_config.get("TIMEOUT", 10)
        try:
            async with async_timeout.timeout(timeout):
                resp = await self._make_request()

            try:
                resp_encoding = resp.get_encoding()
            except:
                resp_encoding = None

            response = Response(
                url=str(resp.url),
                method=resp.method,
                encoding=resp_encoding,
                metadata=self.metadata,
                cookies=resp.cookies,
                headers=resp.headers,
                history=resp.history,
                status=resp.status,
                aws_json=resp.json,
                aws_text=resp.text,
                aws_read=resp.read,
            )
            # Retry middleware
            aws_valid_response = self.request_config.get("VALID")
            if aws_valid_response and iscoroutinefunction(aws_valid_response):
                response = await aws_valid_response(response)
            if response.ok:
                return response
            else:
                return await self._retry(
                    error_msg=f"Request url failed with status {response.status}!"
                )
        except asyncio.TimeoutError:
            return await self._retry(error_msg="timeout")
        except Exception as e:
            return await self._retry(error_msg=e)
        finally:
            # Close client session
            await self._close_request()
