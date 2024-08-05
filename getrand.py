import http.server
import socketserver
import socket
import jinja2
import random
import argparse
import os

class RandHandler(http.server.SimpleHTTPRequestHandler):

	def do_GET(self):
		print("enter do_GET")
		self.protocol_version = "HTTP/1.1"
		self._headers = self.headers
		self._url = self.path
		self.send_response(200)
		# self.send_header("Content-type", "application/html")
		self.end_headers()
		number = random.randint(0, 10000000)
		env = jinja2.Environment()
		template = env.from_string("""
<!DOCTYPE html>
<html>
<head>
  <title>Random number</title>
</head>
<body>
  <p>
    Random number: {{ number }}
  </p>
</body>
</html>

""")
		value = template.render(number = number)
		encoded = value.encode("utf-8")
		output = bytearray(encoded)
		self.wfile.write(output)

def main():
	print("enter main")
	parser = argparse.ArgumentParser(
		prog = "getrand",
		description = "Simple web server",
		argument_default = "8082")
	parser.add_argument("-p", "--port")
	args = parser.parse_args()
	PORT = int(args.port)
	server = RandHandler
	server = socketserver.TCPServer(("", PORT), RandHandler)
	server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# with socketserver.TCPServer(("", PORT), server) as httpd:
	with server as httpd:
		# httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print("serving at port", PORT)
		httpd.serve_forever()

if __name__ == "__main__":
	main()
