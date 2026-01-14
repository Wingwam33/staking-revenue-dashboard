#!/usr/bin/env python3
"""
Simple HTTP server with API endpoint for fetching staking snapshots
"""
import http.server
import socketserver
import urllib.request
import json
import os
from urllib.parse import urlparse

PORT = int(os.environ.get('PORT', 8000))
API_URL = 'https://mefoundation.com/api/trpc/staking.getStakerSnapshot?input=%7B%22json%22%3A%7B%20%22token%22%3A%20%22MEFNBXixkEbait3xn9bkm8WsJzXtVsaJEn4c8Sam21u%22,%20%22ns%22%3A%20%22acAvyneD7adS3yrXUp41c1AuoYoYRhnjeAWH9stbdTf%22%7D%7D'
DATA_FILE = 'staking-data.json'

class StakingServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/fetch-snapshot':
            self.handle_fetch_snapshot()
        else:
            # Serve static files normally
            super().do_GET()

    def handle_fetch_snapshot(self):
        """Fetch snapshot from ME Foundation API and save to file"""
        try:
            # Fetch data from API
            req = urllib.request.Request(
                API_URL,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
            )

            # Disable SSL verification for this request
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, context=ctx) as response:
                data = response.read()

            # Save to file
            with open(DATA_FILE, 'wb') as f:
                f.write(data)

            # Get file size
            file_size = os.path.getsize(DATA_FILE)
            file_size_mb = file_size / (1024 * 1024)

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response_data = {
                'success': True,
                'message': f'Snapshot saved successfully ({file_size_mb:.1f}MB)',
                'file_size': file_size
            }
            self.wfile.write(json.dumps(response_data).encode())

            print(f'✅ Snapshot fetched and saved successfully ({file_size_mb:.1f}MB)')

        except Exception as e:
            print(f'❌ Error fetching snapshot: {str(e)}')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response_data = {
                'success': False,
                'error': str(e)
            }
            self.wfile.write(json.dumps(response_data).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), StakingServerHandler) as httpd:
        print(f"🚀 Staking Dashboard Server running on port {PORT}")
        print(f"📊 Dashboard: /staking-revenue-dashboard.html")
        print(f"📸 Snapshot API: /api/fetch-snapshot")
        print("\nPress Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
