import asyncio
import json
import logging

import aiohttp
from .exception import HTTP_EXCEPTIONS, TransportError

logger = logging.getLogger(__name__)


class Connection:
    """
    Class responsible for maintaining a connection to an Cayley.

    Also responsible for logging.
    """

    def __init__(self, host, port, *, loop):
        self._loop = loop
        self._connector = aiohttp.TCPConnector(resolve=True, loop=loop)
        self._base_url = 'http://{}:{}/'.format(host, port)
        self._request = aiohttp.request

    def close(self):
        self._connector.close()

    @asyncio.coroutine
    def perform_request(self, method, url, params, body):
        url = self._base_url + url
        resp = yield from self._request(method, url,
                                        params=params, data=body,
                                        connector=self._connector,
                                        loop=self._loop)

        resp_body = yield from resp.text()
        if not (200 <= resp.status <= 300):
            extra = None
            try:
                extra = json.loads(resp_body)
            except ValueError:
                pass

            exc_class = HTTP_EXCEPTIONS.get(resp.status, TransportError)
            raise exc_class(resp.status, resp_body, extra)
        return resp.status, resp.headers, resp_body
