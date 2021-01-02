#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/2.
"""
import typing

from ruia import Spider

from ruia_cache.request import RequestCacheSpider


class RuiaCacheSpider(Spider):
    """
    Ruia cache spider
    Adding caching features to Ruia
    """

    def request(
        self,
        url: str,
        method: str = "GET",
        *,
        callback=None,
        encoding: typing.Optional[str] = None,
        headers: dict = None,
        metadata: dict = None,
        request_config: dict = None,
        request_session=None,
        **aiohttp_kwargs,
    ):
        """
        Init a Request class for crawling html
        :param url:
        :param method:
        :param callback:
        :param encoding:
        :param headers:
        :param metadata:
        :param request_config:
        :param request_session:
        :param aiohttp_kwargs:
        :return:
        """
        headers = headers or {}
        metadata = metadata or {}
        request_config = request_config or {}
        request_session = request_session or self.request_session

        headers.update(self.headers.copy())
        request_config.update(self.request_config.copy())
        aiohttp_kwargs.update(self.aiohttp_kwargs.copy())

        req_ins = RequestCacheSpider(
            url=url,
            method=method,
            callback=callback,
            encoding=encoding,
            headers=headers,
            metadata=metadata,
            request_config=request_config,
            request_session=request_session,
            **aiohttp_kwargs,
        )
        req_ins.spider_name = self.name
        return req_ins
