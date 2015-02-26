import asyncio
import time
import unittest


from aiocayley.transport import Transport


class TestTransport(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_transport(self, host='localhost', port=64210):
        tr = Transport(host, port, loop=self.loop)
        self.addCleanup(tr.close)
        return tr

    def test_simple(self):
        tr = self.make_transport()

        @asyncio.coroutine
        def go():
            status, data = yield from tr.perform_request(
                'POST', 'api/v1/query/gremlin', body='g.Emit("test")')
            self.assertEqual(200, status)
            self.assertIn('test', data['result'])
        self.loop.run_until_complete(go())
