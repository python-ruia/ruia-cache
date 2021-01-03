# ruia-cache

A [Ruia](https://github.com/howie6879/ruia) plugin for caching URL

## Installation

```shell script
pip install -U ruia-cache

# New features
pip install git+https://github.com/python-ruia/ruia-cache
```

## Usage

`ruia-cache` will automatically cache the captured URL to prevent the second request to the target web page:

```python
import os

from ruia_cache import RuiaCacheSpider

# Set RUIA_CACHE path
os.environ.setdefault(
    "RUIA_CACHE", os.path.dirname(__file__),
)


class Demo(RuiaCacheSpider):
    name = "demo_spider"
    start_urls = ["http://httpbin.org/get"]

    async def parse(self, response):
        html = await response.text()
        print(html)


if __name__ == "__main__":
    Demo.start()
    # Using cache data
    Demo.start()
```

Enjoy it :)