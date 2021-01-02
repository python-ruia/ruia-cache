#!/usr/bin/env python
"""
 Created by howie.hu at 2021/1/1.
"""
import os

from ruia_cache import RuiaCacheSpider

# Set RUIA_CACHE path
os.environ.setdefault(
    "RUIA_CACHE", os.path.dirname(__file__),
)


class Demo(RuiaCacheSpider):
    name = "demo_spider"
    # start_urls = ["http://httpbin.org/get", "http://httpbin.org/get"]
    start_urls = ["http://httpbin.org/get"]

    async def parse(self, response):
        html = await response.text()
        print(html)


if __name__ == "__main__":
    Demo.start()
    Demo.start()
