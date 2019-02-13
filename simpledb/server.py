from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

from collections import namedtuple
from io import BytesIO
from socket import error as socket_error


# we'll use exceptions to notify the conn handling loop of problems
class CommandError(Exception): pass
class Disconnect(Exception): pass

Error = namedtuple('Error', ('message',))

class ProtocolHandler(object):
    def handle_request(self, socket_file):
        # Parse a request from client into its cmpnt parts
        pass

    def write_responses(self, socket_file, data):
        # serialize the response data and send it to the client
        pass


class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=64):
        self._pool = Pool(max_clients)
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self._pool)
        self._protocol = ProtocolHandler()
        self._kv = {}

    
    def connection_handler(self, conn, address):
        # Convert "conn" (a socket object) into a file-like object
        socket_file = conn.makefile('rwb')

        # process client requests until client disconnects
        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnect:
                break
            
            try:
                resp = self.get_response(data)
            except CommandError as exc:
                resp = Error(exc.args[0])
        
        self._protocol.write_responses(socket_file, resp)
    
    def get_response(self, data):
        # here we actually unpack the data sent by the client, execute
        # the cmd they specified, and pass back the return value
        pass
    
    def run(self):
        self._server.serve_forever()
