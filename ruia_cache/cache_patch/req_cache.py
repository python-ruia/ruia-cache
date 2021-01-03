#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/3.
"""
import os

from functools import wraps

import aiofiles

from ruia import Response

from ruia_cache.serializers import PickleSerializer
from ruia_cache.utils import create_cache_dir, gen_cache_dir, logger, md5_encryption


def req_cache(*args, **kwargs):
    """
    Cache decorate for `ruia.Request` class
    :param args:
    :param kwargs:
    :return:
    """

    fetch_func = args[0]

    @wraps(fetch_func)
    async def wrapper(self, delay=True):
        cache_resp = None

        url_str = f"{self.url}:{self.method}"
        req_url_str = f"{url_str}:{self.request_config}"

        # Check whether the current path exists
        cache_path = gen_cache_dir()
        pro_dir = os.path.join(cache_path, self.spider_name)
        if not os.path.exists(pro_dir):
            create_cache_dir(pro_dir)

        req_file = f"{md5_encryption(string=req_url_str)}_req.ruia"
        resp_file = f"{md5_encryption(string=url_str)}_resp.ruia"

        req_url_path = os.path.join(pro_dir, req_file)
        resp_url_path = os.path.join(pro_dir, resp_file)

        pickle_ins = PickleSerializer()

        if os.path.exists(req_url_path) and os.path.exists(resp_url_path):
            # Get data locally
            try:
                async with aiofiles.open(req_url_path, mode="rb") as f:
                    s_data = await f.read()
                data = pickle_ins.loads(s_data)
                cache_resp = data["cache_resp"]
            except Exception as e:
                logger.error(
                    f"<Cache load failed: url: {self.url}, method: {self.method}, err: {e}>"
                )
        else:
            # Delete already path
            os.remove(req_url_path) if os.path.exists(req_url_path) else None
            os.remove(resp_url_path) if os.path.exists(resp_url_path) else None

            # Make a request
            resp: Response = await fetch_func(self, delay)

            try:
                from ruia_cache.response import CacheResponse

                cache_resp = CacheResponse(
                    url=resp.url,
                    method=resp.method,
                    encoding=resp.encoding,
                    metadata=resp.metadata,
                    cookies=resp.cookies,
                    headers=dict(resp.headers),
                    history=resp.history,
                    status=resp.status,
                    aws_json=None,
                    aws_text=None,
                    aws_read=None,
                )
                cache_resp.spider_name = self.spider_name
                data = {
                    "cache_resp": cache_resp,
                    # "expire_time": time.time() + ttl,
                    # "ttl": ttl,
                }
                s_data = pickle_ins.dumps(data)
                # Persist target data
                async with aiofiles.open(req_url_path, mode="wb+") as f:
                    await f.write(s_data)
                logger.info(
                    f"<Cache serialization successfully: "
                    f"cache_path: {req_url_path} [url: {resp.url}, method: {resp.method}]>"
                )
                cache_resp._source_resp = resp

            except Exception as e:
                logger.error(
                    f"<Cache serialization failed: url: {resp.url}, method: {resp.method}, err: {e}>"
                )

        return cache_resp

    return wrapper
