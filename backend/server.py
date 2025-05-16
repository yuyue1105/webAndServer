from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.handle_static_files()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404,'Not Found')
    
    def handle_static_files(self):
        path = self.path
        if path == '/':
            path = '/index.html'
        if '..' in path:
            self.send_error(403,'Forbidden')
            return
        try:
            full_path = os.path.join('frontend',path.lstrip('/'))
            if not os.path.exists(full_path):
                self.send_error(404,'File Not Found')
                return
            content_type = 'text/html'
            if full_path.endswit('.css'):
                content_type = 'text/css'
            elif full_path.endswith('.js'):
                content_type = 'application/javascript'
            with open(full_path,'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except Exception as e:
            self.send_error(500,f'Server Error:{str(e)}')
    def handle_api_request(self):
        if self.path == '/api/submit' and self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                response = {
                    'status': 'success',
                    'message': '数据接收成功',
                    'receivedData':data
                }
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfilewrite(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_error(400,'Bad Request:Invalid JSON')
        else:
            self.send_error(404,'Not Found')
def run_server():
    host = 'localhost'
    port = 8000
    server = HTTPServer((host,port),RequestHandler)
    print(f'服务器运行在 http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('服务器已关闭')
if __name__ =='__main__':
    run_server