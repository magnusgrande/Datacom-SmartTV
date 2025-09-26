import socket


class RemoteControlClient:
    """Client class to interact with the Smart TV server."""

    def __init__(self, host='localhost', port=1238):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_and_receive(self, sock, message):
        """Sends a message to the server and waits for a response."""
        self.sock.sendall((message + "\n").encode())
        data = b""
        while not data.endswith(b"\n"):
            more = sock.recv(1024)
            if not more:
                break
            data += more
        return data.decode().strip()

    def close(self):
        """Closes the socket connection."""
        self.sock.close()
