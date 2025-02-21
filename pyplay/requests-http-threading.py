import json
import threading
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """
        Successfully handle any POST request
        """
        content_length = int(self.headers["Content-Length"])
        assert self.headers["Content-Type"] == "application/json"
        assert self.headers["Croix-Header"] == "croix forever"
        body = self.rfile.read(content_length)
        print("Received json:", body.decode())
        self.send_response(200)
        self.send_header("Croix-Back", "croix indeed")
        self.end_headers()
        self.wfile.write(b"OK")


def start_server():
    server = HTTPServer(("localhost", 8000), MyHandler)
    server.serve_forever()


# daemon=True means python can immediately kill this thread on process stop without
# waiting for it to finish up anything
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# GET request
url = "http://localhost:8000/data/hello.json"
headers = {"Accept": "application/json"}
resp = requests.get(url=url, headers=headers)
resp_json = json.loads(resp.text)

assert resp.status_code == 200
assert resp_json["hello"] == "world"
assert resp.headers["Content-Type"] == "application/json"

# POST
url = "http://localhost:8000/good"
headers = {"Content-Type": "application/json", "Croix-Header": "croix forever"}
# alternately, instead of data=, provide json= parameter
resp = requests.post(url=url, headers=headers, data=resp.text)
assert resp.status_code == 200
assert resp.headers["Croix-Back"] == "croix indeed"

# bad GET
url = "http://localhost:8000/junk"
resp = requests.get(url=url)
assert resp.status_code == 404
