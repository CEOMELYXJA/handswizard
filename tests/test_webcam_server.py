import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
import webcam_server as server
from mouse_core import MouseController

class FakeMouse:
    def __init__(self): self.events = []
    def mouseDown(self, button): self.events.append(('down', button))
    def mouseUp(self, button): self.events.append(('up', button))
    def moveRel(self, *args, **kwargs): pass
    def click(self, button): pass
    def scroll(self, n): pass

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        server.PORT = cls.http.server_address[1]
        threading.Thread(target=cls.http.serve_forever, daemon=True).start()
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown(); cls.http.server_close()
    def setUp(self):
        self.mouse = FakeMouse()
        server.controller = MouseController(self.mouse)
    def request(self, payload, token=None, origin=None, host=None):
        c = http.client.HTTPConnection('127.0.0.1', server.PORT)
        headers = {'Host': host or f'127.0.0.1:{server.PORT}', 'Origin': origin or f'http://127.0.0.1:{server.PORT}', 'X-Handswizard-Token': token or server.TOKEN, 'Content-Type':'application/json'}
        c.request('POST', '/command', json.dumps(payload), headers)
        response = c.getresponse(); response.read(); c.close(); return response.status
    def test_origin_token_and_host_rejected(self):
        for kw in ({'origin':'https://evil.example'}, {'token':'wrong'}, {'host':'evil.example'}):
            self.assertEqual(self.request({'type':'resume'}, **kw), 403)
        self.assertTrue(server.controller.paused)
    def test_authorized_drag_released_on_pause(self):
        self.assertEqual(self.request({'type':'resume'}), 200)
        self.assertEqual(self.request({'type':'button','button':'left','down':True}), 200)
        self.assertEqual(self.request({'type':'pause'}), 200)
        self.assertEqual(self.mouse.events, [('down','left'),('up','left')])

if __name__ == '__main__': unittest.main()
