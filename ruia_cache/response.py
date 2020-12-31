#!/usr/bin/env python
"""
 Created by howie.hu at 2020/12/31.
"""
import json

from typing import Any, Callable, Optional

from ruia import Response

DEFAULT_JSON_DECODER = json.loads
JSONDecoder = Callable[[str], Any]


class RuiaCacheResponse(Response):
    """
    Ruia Cache Class for Response
    """

    async def json(
        self,
        *,
        encoding: str = None,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        content_type: Optional[str] = "application/json",
    ) -> Any:
        """Read and decodes JSON response."""
        encoding = encoding or self._encoding
        return await self._aws_json(
            encoding=encoding, loads=loads, content_type=content_type
        )

    async def text(
        self, *, encoding: Optional[str] = None, errors: str = "strict"
    ) -> str:
        """Read response payload and decode."""
        encoding = encoding or self._encoding
        self._html = await self._aws_text(encoding=encoding, errors=errors)
        return self._html
