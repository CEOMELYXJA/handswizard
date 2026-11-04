"""Passerelle webcam locale : aucun paquet Python externe."""
import ctypes.wintypes
import hmac
import json
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from mouse_core import MouseController
from windows_mouse import WindowsMouse

HOST, PORT = '127.0.0.1', 8765
ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
controller = None
lock = threading.RLock()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def trusted(self):
        return (self.headers.get('Host') == f'{HOST}:{PORT}' and
                self.headers.get('Origin') == f'http://{HOST}:{PORT}' and
                hmac.compare_digest(self.headers.get('X-Handswizard-Token', ''), TOKEN))
    def do_GET(self):
        if self.headers.get('Host') != f'{HOST}:{PORT}':
            self.send_error(403); return
        path = self.path.split('?', 1)[0]
        files = {'/': ('webcam.html', 'text/html; charset=utf-8'), '/webcam.js': ('webcam.js', 'text/javascript; charset=utf-8')}
        if path not in files:
            self.send_error(404); return
        name, mime = files[path]
        content = (ROOT / name).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'self' https://cdn.jsdelivr.net 'wasm-unsafe-eval'; connect-src 'self' https://cdn.jsdelivr.net https://storage.googleapis.com; style-src 'unsafe-inline'; img-src 'self' data:; media-src 'self' blob:; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers(); self.wfile.write(content)
    def do_POST(self):
        if self.path != '/command' or not self.trusted():
            self.send_error(403); return
        try:
            n = int(self.headers.get('Content-Length', '0'))
            if n < 1 or n > 512: raise ValueError()
            data = json.loads(self.rfile.read(n))
            with lock: ok = controller.dispatch(data)
        except (ValueError, TypeError):
            self.send_error(400); return
        self.send_response(200 if ok else 400)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()

def watchdog():
    while True:
        time.sleep(.2)
        with lock: controller.watchdog()

def main():
    global controller
    controller = MouseController(WindowsMouse())
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    threading.Thread(target=watchdog, daemon=True).start()
    print('Handswizard webcam : laisse cette fenêtre ouverte. Ctrl+C pour arrêter.')
    webbrowser.open(f'http://{HOST}:{PORT}/#{TOKEN}')
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally:
        with lock: controller.stop()
        server.server_close()

if __name__ == '__main__': main()
