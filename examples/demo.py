#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""
import os

from ruia_cache import RuiaCacheSpider

# Set RUIA_CACHE path
os.environ.setdefault(
    "RUIA_CACHE", "/Users/howie6879/Documents/Programming/Python/git/ruia-cache/",
)
# set RUIA_CACHE_TTL
os.environ.setdefault(
    "RUIA_CACHE_TTL", "3600",
)


class Demo(RuiaCacheSpider):
    name = "demo_spider"
    start_urls = ["http://httpbin.org/get", "http://httpbin.org/get"]

    async def parse(self, response):
        print(await response.text())


if __name__ == "__main__":
    Demo.start()
