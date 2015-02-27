import asyncio
import json

from .connection import Connection
from .exception import ConnectionError


class Transport:
    """Encapsulation of transport-related to logic.

    Main interface is the `perform_request` method.

    """

    def __init__(self, host, port, *, loop):
        self._loop = loop
        self._connection = Connection(host, port, loop=self._loop)

    def close(self):
        self._connection.close()

    @asyncio.coroutine
    def get_connection(self):
        """
        Retreive a :class:`~aioes.Connection` instance from the
        :class:`~aioes.Connection` instance.
        """
        return self._connection

    @asyncio.coroutine
    def perform_request(self, method, url, params=None, body=None,
                        *, request_timeout=None, decoder=json.loads):
        """
        :arg method: HTTP method to use
        :arg url: absolute url (without endpoint) to target
        :arg params: dictionary of query parameters, will be handed over to the
          underlying :class:`~elasticsearch.Connection` class for serialization
        :arg body: body of the request, will be serializes using serializer and
            passed to the connection
        """
        if body is not None:
            if not isinstance(body, (str, bytes)):
                body = json.dumps(body)
            body = body.encode('utf-8')

        connection = yield from self.get_connection()
        try:
            status, headers, data = yield from asyncio.wait_for(
                connection.perform_request(
                    method,
                    url,
                    params,
                    body),
                request_timeout,
                loop=self._loop)
        except ConnectionError:
            raise
        else:
            if data:
                data = decoder(data)
        return status, data
