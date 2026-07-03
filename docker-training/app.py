from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define a request handler that responds to HTTP GET requests.
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Send an HTTP 200 OK status code.
        self.send_response(200)
        # Set the response content type header to HTML.
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Write the HTML response body to the client.
        self.wfile.write(b"<h1>Hello World! Docker is working!</h1>")

# Create an HTTP server listening on all interfaces at port 5000,
# using the custom request handler above.
server = HTTPServer(('0.0.0.0', 5000), MyHandler)
print("Server started on port 5000...")

# Start the server loop so it handles incoming requests forever.
server.serve_forever()