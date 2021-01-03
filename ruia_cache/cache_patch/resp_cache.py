#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/3.
"""

import os

from functools import wraps

import aiofiles


from ruia_cache.serializers import PickleSerializer
from ruia_cache.utils import create_cache_dir, gen_cache_dir, logger, md5_encryption


def resp_cache(*args, **kwargs):
    """
    Cache decorate for `ruia.Response` class
    :param args:
    :param kwargs:
    :return:
    """

    func = args[0]

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        target_func_res = None
        url_str = f"{self.url}:{self.method}"
        target_func_name = func.__name__
        # Check whether the current path exists
        cache_path = gen_cache_dir()
        pro_dir = os.path.join(cache_path, self.spider_name)
        if not os.path.exists(pro_dir):
            create_cache_dir(pro_dir)
        resp_file = f"{md5_encryption(string=url_str)}_resp.ruia"
        resp_url_path = os.path.join(pro_dir, resp_file)

        pickle_ins = PickleSerializer()

        async def save_s_data(data, data_path):
            """
            Serialize and persist data
            :param data:
            :param data_path:
            :return:
            """
            # Persist target data
            async with aiofiles.open(data_path, mode="wb+") as f:
                await f.write(pickle_ins.dumps(data))
            logger.info(
                f"<Cache serialization successfully: "
                f"cache_path: {data_path} [url: {self.url}, method: {self.method}]>"
            )

        if os.path.exists(resp_url_path):
            # Get data locally
            try:
                async with aiofiles.open(resp_url_path, mode="rb") as f:
                    s_data = await f.read()
                data: dict = pickle_ins.loads(s_data)
                target_func_res = data.get(target_func_name)
                if target_func_res is None:
                    target_func_res = await func(self)
                    data.update({target_func_name: target_func_res})
                    await save_s_data(data=data, data_path=resp_url_path)

            except Exception as e:
                logger.error(
                    f"<Cache load failed: url: {self.url}, method: {self.method}, err: {e}>"
                )
        else:
            target_func_res = await func(self)
            data = {target_func_name: target_func_res}
            await save_s_data(data=data, data_path=resp_url_path)

        return target_func_res

    return wrapper