import http.server
import os
import sys

docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "docs"))
if not os.path.exists(docs_dir):
    docs_dir = os.path.abspath("docs")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=docs_dir, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

server = http.server.ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
print(f"Serving {docs_dir} on http://127.0.0.1:8000")
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
