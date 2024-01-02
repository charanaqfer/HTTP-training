from http.server import SimpleHTTPRequestHandler
import http.cookies

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if the 'my_cookie' is present in the request
        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        print(cookies)
        # Check if the '__intern' cookie is present
        if '__intern' in cookies:
            # If the cookie is present, return a 204 response
            self.send_response(204)
            self.end_headers()
        else:
            # If the cookie is not present, set a new cookie and return a 200 response
            cookie = http.cookies.SimpleCookie()
            cookie['__intern'] = 1234
            cookie_string = cookie.output(header='', sep=';')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', cookie_string)
            self.end_headers()

            # Your response body goes here
            self.wfile.write(b'Hello, HTTP Server!')

if __name__ == '__main__':
    from http.server import HTTPServer
    server_address = ('', 9090)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server running on http://localhost:9090/')
    httpd.serve_forever()
