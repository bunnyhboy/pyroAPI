from wsgiref.simple_server import make_server
from app import app  # bumbo app ko instance form yeha import hunxa

PORT = 8000

with make_server('', PORT, app) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
