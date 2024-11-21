from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Đang chạy server tại http://localhost:{port}/')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nTắt server...')
        httpd.server_close()
        sys.exit(0)

if __name__ == '__main__':
    run()
