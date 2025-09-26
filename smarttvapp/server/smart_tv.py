class SmartTV:
    """Represents a Smart TV."""

    def __init__(self):
        # Set the initial state of the TV
        self.state_is_on = False
        self.state_current_channel = 1
        self.state_previous_channel = 1
        self.state_number_of_channels = 10

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
                if value == "up":
                    if (self.state_current_channel <
                        self.state_number_of_channels):
                        self.state_previous_channel = (
                            self.state_current_channel)
                        self.state_current_channel += 1
                    else:
                        return (f"Error: Already at the highest channel "
                                f"({self.state_number_of_channels}).")
                elif value == "down":
                    if self.state_current_channel > 1:
                        self.state_previous_channel = self.state_current_channel
                        self.state_current_channel -= 1
                    else:
                        return "Error: Already at the lowest channel (1)."
                else:
                    return "Error: Invalid channel command. Use 'up' or 'down'."
            else:
                return "Error: Unknown attribute. Use 'power' or 'channel'."
            return "state " + str(self.get_state("full"))

        except ValueError:
            return ("Error: Invalid command format. "
                    "Use 'set <attribute> <value>'.")
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
        if not self.state_is_on:
            return "The TV is off. Please turn it on first."

        if detail == "power":
            return "on" if self.state_is_on else "off"
        elif detail == "channel":
            return (str(self.state_current_channel) +
                    "/" +
                    str(self.state_number_of_channels))
        elif detail == "channels":
            return str(self.state_number_of_channels)
        elif detail == "full":
            return (f"power: {'On' if self.state_is_on else 'Off'}\n"
                    f"channel: {self.state_current_channel}\n"
                    f"total channels: {self.state_number_of_channels}")
        else:
            return ("Error: Unknown detail level. "
                    "Use 'full', 'power', 'channel', or 'channels'.")
