import socket


# TODO: implement Signal handling to gracefully shutdown the server


class SmartTV:
    """Represents a Smart TV with power on/off and channel switching."""

    def __init__(self):
        # Set the initial state of the TV
        self.state_is_on = False
        self.state_current_channel = 1
        self.state_previous_channel = 1
        self.state_number_of_channels = 100

    def run(self):
        """Starts the server to listen for incoming connections."""
        # Initialize server socket to avoid TypeError when attempting to close.
        server_socket = None
        try:
            # Open a socket to listen for incoming connections
            # Listens on localhost:1337
            # TODO: Part 3: Support multiple concurrent connections.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("localhost", 1337))
            server_socket.listen(1)
            print("SmartTV server is running on localhost:1337")
        # TODO: Handle exceptions better
        except Exception as e:
            print(f"Could not start listening: {e}")
            return
        try:
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"Connection with {addr} has been established!")
                    self.handle_client(client_socket)
                # TODO: Handle exceptions better
                except Exception as e:
                    print(f"Error: {e}")
        finally:
            # Ensure the socket exists before attempting to close.
            if server_socket:
                server_socket.close()
                print("Server socket closed.")

    def handle_client(self, client_socket):
        """Handles communication with a connected client."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_message = data.decode().strip()

                # Handles state retrieval
                if client_message == "get":
                    response = "Current state: " + self.get_state("full")

                # Handles state change
                elif client_message.startswith("set"):
                    response = self.handle_state_change_request(client_message)
                else:
                    response = "Error: Unknown command. Please try again."
                client_socket.sendall((response + "\n").encode())
        # Handle client disconnects gracefully
        except ConnectionResetError as e:
            print(f"Error: Connection forcibly closed by the client: {e}")
        finally:
            client_socket.close()

    def handle_state_change_request(self, client_message):
        """Handles state change requests from client messages.

        Returns the updated state of the TV, if any,
            or an error if the command fails to update the state.
        """

        try:
            # split the message, first part ('set') was used to enter
            # this function and is therefore ignored
            # TODO: Return more granular update messages.
            #       i.e. "power was already on",
            #            "channel changed from 1 to 2"
            _, attribute, value = client_message.split()

            # Ensure the TV is on before changing state
            if not self.state_is_on and attribute != "power":
                return ("Error: The TV is off. Please turn it on first. "
                        "<set power on>")

            if attribute == "power":
                if value == "on":
                    if not self.state_is_on:
                        self.state_is_on = True
                elif value == "off":
                    if self.state_is_on:
                        self.state_is_on = False
                else:
                    return "Error: Invalid power state. Use 'on' or 'off'."

            elif attribute == "channel":
                value = int(value)
                if 1 <= value <= self.state_number_of_channels:
                    self.state_previous_channel = self.state_current_channel
                    self.state_current_channel = value
                else:
                    return f"Error: Invalid channel number. Use a number between 1 and {self.state_number_of_channels}."

            else:
                return "Error: Unknown attribute. Use 'power' or 'channel'."
            return "state " + str(self.get_state("full"))

        except ValueError:
            return "Error: Invalid command format. Use 'set <attribute> <value>'."
        except Exception as e:
            return f"Error: {e}"

    def get_state(self, detail="full"):
        """Returns the current state of the TV as a string.
            The detail parameter defines what information to return:
                full - returns the full state (as a string)
                power - returns only the power state (as a string <on/off>)
                channel - returns the current channel (as a string)
                channels - returns the number of channels (as a string)
                DEFAULT: full
        """
        if detail == "power":
            return "on" if self.state_is_on else "off"
        elif detail == "channel":
            return str(self.state_current_channel)
        elif detail == "channels":
            return str(self.state_number_of_channels)
        else:
            return (f"power: {'on' if self.state_is_on else 'off'}, "
                    f"channel: {self.state_current_channel}, "
                    f"total channels: {self.state_number_of_channels}")


if __name__ == "__main__":
    tv = SmartTV()
    tv.run()
