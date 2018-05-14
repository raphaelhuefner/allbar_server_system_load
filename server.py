import http.server
import socketserver
import threading

import payload

class MiniDiagramHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        config = payload.get()
        self.send_response(200, message='OK')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(config))
        self.end_headers()
        self.wfile.write(config)

server = None

def run(ip='127.0.0.1', port=8000):
    global server
    server = socketserver.ThreadingTCPServer((ip, port), MiniDiagramHandler)
    with server:
        ip, port = server.server_address
        print("Serving at http://{ip}:{port}/".format(ip=ip, port=port))
        server.serve_forever()

def shutdown():
    global server
    if hasattr(server, 'shutdown') and callable(server.shutdown):
        server.shutdown()
