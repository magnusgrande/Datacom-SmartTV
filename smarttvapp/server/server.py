import socket
import threading
from smart_tv import SmartTV
from protocol import handle_protocol


class ClientHandler:
    """Handles a client connection."""

    def __init__(self, conn, addr, tv, client_id):
        self.conn = conn
        self.addr = addr
        self.tv = tv
        self.client_id = client_id

    def handle_client(self):
        """Handles communication with a connected client."""
        print(f"Client {self.client_id} ({self.addr}) started handling")
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    print(f"Client {self.client_id} ({self.addr}) disconnected")
                    break

                client_message = data.decode().strip()
                print(f"Client {self.client_id} sent: {client_message}")

                response = handle_protocol(self.tv, client_message)
                self.conn.sendall((response + "\n").encode())

        except ConnectionResetError as e:
            print(f"Client {self.client_id} ({self.addr}) connection reset: {e}")
        except Exception as e:
            print(f"Error handling client {self.client_id} ({self.addr}): {e}")
        finally:
            print(f"Closing connection for client {self.client_id} ({self.addr})")
            self.conn.close()


def main():
    """Main function to run the server."""
    tv = SmartTV()
    client_counter = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow socket reuse to avoid "Address already in use" errors
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', 1238))
        server_socket.listen(5)  # Allow up to 5 pending connections
        print("SmartTV server is listening on localhost:1238")
        print("Multiple clients can now connect simultaneously!")

        try:
            while True:
                conn, addr = server_socket.accept()
                client_counter += 1
                print(f"Client {client_counter} connected from {addr}")

                handler = ClientHandler(conn, addr, tv, client_counter)
                thread = threading.Thread(
                    target=handler.handle_client,
                    daemon=True,
                    name=f"Client-{client_counter}"
                )
                thread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Server error: {e}")


if __name__ == "__main__":
    main()
