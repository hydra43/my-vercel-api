from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # তোমার এপিআই রেসপন্স ডাটা
        response_data = {
            "status": "success",
            "message": "হ্যালো! এটি ভার্সেল থেকে রান হওয়া আমার পার্সোনাল পাইথন এপিআই।"
        }

        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
