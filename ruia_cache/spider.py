#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""
import os
import time
import typing

from functools import wraps
from types import AsyncGeneratorType

from ruia import Request, Response, Spider
from ruia.exceptions import NothingMatchedError, NotImplementedParseError
from ruia_cache.serializers import PickleSerializer
from ruia_cache.utils import create_cache_dir, gen_cache_dir, logger, md5_encryption

global_dict = {}


def cache(*args, **kwargs):

    handle_request = args[0]

    @wraps(handle_request)
    async def wrapper(self, request: Request):
        string = f"{request.url}:{request.method}:{request.request_config}:{request.aiohttp_kwargs}"
        # Check whether the current path exists
        cache_path = gen_cache_dir()
        pro_dir = os.path.join(cache_path, self.name)
        if not os.path.exists(pro_dir):
            create_cache_dir(pro_dir)
        md5_key = md5_encryption(string=string)
        print(md5_key)
        ttl = int(os.getenv("RUIA_CACHE_TTL", 86400))
        is_exist = 1 if md5_key in global_dict.keys() else 0
        print(is_exist)
        if is_exist:
            callback_result, response = global_dict[md5_key][0:2]
        else:
            callback_result, response = await handle_request(self, request)
            expire_time = time.time() + ttl
            data = [callback_result, response, expire_time]
            try:
                global_dict[md5_key] = data
            except Exception as e:
                logger.exception(e)
        print(global_dict)
        return callback_result, response

    return wrapper


class RuiaCacheSpider(Spider):
    """
    Ruia cache spider
    Adding caching features to Ruia
    """

    pickle_ins = PickleSerializer()

    @cache
    async def handle_request(
        self, request: Request
    ) -> typing.Tuple[AsyncGeneratorType, Response]:
        """
        Wrap request with middleware.
        :param request:
        :return:
        """
        callback_result, response = None, None
        try:
            await self._run_request_middleware(request)
            callback_result, response = await request.fetch_callback(self.sem)
            await self._run_response_middleware(request, response)
            await self._process_response(request=request, response=response)
        except NotImplementedParseError as e:
            self.logger.exception(e)
        except NothingMatchedError as e:
            error_info = f"<Field: {str(e).lower()}" + f", error url: {request.url}>"
            self.logger.exception(error_info)
        except Exception as e:
            self.logger.exception(f"<Callback[{request.callback.__name__}]: {e}")

        return callback_result, response
