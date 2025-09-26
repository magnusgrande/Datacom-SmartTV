import socket
import threading
from smart_tv import SmartTV

class ClientHandler:
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
                if client_message == "get":
                    response = "Current state: " + "\n" + self.tv.get_state("full")
                elif client_message.startswith("set"):
                    response = self.tv.handle_state_change_request(client_message)
                else:
                    response = "Error: Unknown command. Please try again."
                self.client_socket.sendall((response + "\n").encode())
        except ConnectionResetError as e:
            print(f"Error: Connection forcibly closed by the client: {e}")
        finally:
            self.client_socket.close()

def main():
    tv = SmartTV()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost',1238))
        server_socket.listen()
        print("SmartTV server is listening on localhost:1238")
        while True:
            conn,addr = server_socket.accept()
            print(f"Connection with {addr} has been established!")
            handler = ClientHandler(conn, tv, client_socket=conn)
            thread = threading.Thread(target=handler.handle_client, daemon=True)
            thread.start()

if __name__ == "__main__":
    main()
