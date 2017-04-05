import time

import socketserver


class udp_handler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip().decode("utf-8")
        socket = self.request[1]
        response = eval( str(data))
        socket.sendto(str(response).encode("utf-8"), self.client_address)


class socket_host():
    def __init__(self):
        HOST, PORT = "localhost", 9999
        server = socketserver.UDPServer((HOST, PORT), udp_handler)
        server.serve_forever()
