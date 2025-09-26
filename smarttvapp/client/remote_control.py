from client import RemoteControlClient


def main():
    """Main function to run the remote control client."""
    client = RemoteControlClient()
    try:
        print("Connected to the server.")
        print("Enter 'get' to retrieve the current state.")
        print("Enter 'set <property> <value>' to change a property.")
        print("Valid properties: power (on/off), channel (up/down).")
        print("Enter 'quit' to exit.")
        while True:
            command = input("> ").strip()
            if command.lower() == "exit" or command == "quit":
                print("Exiting remote control.")
                break
            response = client.send_and_receive(client.sock, command)
            print("Response from server:", response)
    except KeyboardInterrupt:
        print("\nExiting remote control.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
