# sentinel/metrics_server.py

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from sentinel.metrics import render

HOST = "127.0.0.1"
PORT = 9105


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return

        output = render().encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        self.wfile.write(output)

    def log_message(self, format, *args):
        # Supress default HTTP request logging
        return


def start_metrics_server():

    def _run():
        try:
            server = HTTPServer((HOST, PORT), MetricsHandler)
            server.serve_forever()
        except Exception:
            # Metrics failure must never crash Sentinel
            pass

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
