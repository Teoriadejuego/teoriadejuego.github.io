"""Loopback-only preview; never launches a visible browser."""
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import argparse


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.webp': 'image/webp',
                      '.js': 'text/javascript', '.css': 'text/css', '.bib': 'text/plain'}

    def log_message(self, format, *args):
        pass  # Do not record query values, even in a local development preview.


@contextmanager
def preview(directory, port=0):
    directory = Path(directory).resolve()
    server = ThreadingHTTPServer(('127.0.0.1', port), partial(Handler, directory=str(directory)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_port)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8078)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parents[1] / 'public')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(args.directory.resolve())))
    print('Preview: http://127.0.0.1:' + str(server.server_port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
