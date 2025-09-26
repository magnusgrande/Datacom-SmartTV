import socket
import threading
from smart_tv import SmartTV
from protocol import handle_protocol


class ClientHandler:
    """Handles a client connection."""

    def __init__(self, conn, tv, client_socket):
        self.conn = conn
        self.tv = tv
        self.client_socket = client_socket

    def handle_client(self):
        """Handles communication with a connected client."""
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                client_message = data.decode().strip()
                response = handle_protocol(self.tv, client_message)
                self.client_socket.sendall((response + "\n").encode())
        except ConnectionResetError as e:
            print(f"Error: Connection forcibly closed by the client: {e}")
        finally:
            self.client_socket.close()


def main():
    """Main function to run the server."""
    tv = SmartTV()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 1238))
        server_socket.listen()
        print("SmartTV server is listening on localhost:1238")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection with {addr} has been established!")
            handler = ClientHandler(conn, tv, client_socket=conn)
            thread = threading.Thread(target=handler.handle_client, daemon=True)
            thread.start()


if __name__ == "__main__":
    main()
