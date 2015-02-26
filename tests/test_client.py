import asyncio
import unittest
from aiocayley import Cayley
from aiocayley.exception import (NotFoundError, ConflictError,
                                 RequestError, TransportError)

import pprint
pp = pprint.pprint


class TestClient(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Cayley('localhost', loop=self.loop)
        self.addCleanup(self.cl.close)

    def tearDown(self):
        self.loop.close()

    def test_simple_query(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.query('g.Emit("simple query").All()')
            self.assertEqual(["simple query"], data['result'])
        self.loop.run_until_complete(go())
        self.cl.__repr__()

    def test_simple_query2(self):
        @asyncio.coroutine
        def go():
            data = yield from self.cl.query(
                'g.V("фильм").Out("synonym").In("synonym").All()')
            print(data)
        self.loop.run_until_complete(go())

