import asyncio
import json
from aiocayley.transport import Transport


default = object()


class Cayley:
    def __init__(self, host, port=64210, *, loop=None, **kwargs):
        self._transport = Transport(host, port, loop=loop, **kwargs)

    @property
    def transport(self):
        return self._transport

    def __repr__(self):
        return "<Cayley [{}]".format(self.transport)

    def _bulk_body(self, body):
        return '\n'.join(map(json.dumps, body)) + '\n'

    def close(self):
        self.transport.close()

    @asyncio.coroutine
    def info(self):
        """
        Get the basic info from the current cluster.
        """
        _, data = yield from self.transport.perform_request('GET', '/')
        return data

    @asyncio.coroutine
    def query(self, query):
        """
        Send query.
        """
        _, data = yield from self.transport.perform_request(
            'POST', 'api/v1/query/gremlin', body=query)
        return data
