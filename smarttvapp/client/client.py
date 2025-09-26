import socket

def main():
    """Main function to run the remote control client."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 1337))
        # TODO: Extract UI elements to CLUI class.
        print("Connected to the server.")
        print("Enter 'get' to retrieve the current state.")
        print("Enter 'set <property> <value>' to change a property.")
        print("Valid properties: power (on/off), channel (1-100).")
        print("Enter 'exit' to quit.")

        while True:
            command = input("> ").strip()
            if command.lower() == "exit":
                print("Exiting the client.")
                break
            if command == "":
                continue
            response = send_and_receive(sock, command)
            print("Server: ", response)

        sock.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def send_and_receive(sock, message):
    """Sends a message to the server and waits for a response."""
    sock.sendall((message + "\n").encode())
    data = b""
    while not data.endswith(b"\n"):
        more = sock.recv(1024)
        if not more:
            break
        data += more
    return data.decode().strip()

if __name__ == "__main__":
    main()