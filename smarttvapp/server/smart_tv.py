class SmartTV:
    """Represents a Smart TV."""

    def __init__(self):
        self.state_is_on = False
        self.state_current_channel = 1
        self.state_previous_channel = 1
        self.state_number_of_channels = 10

    def set_power(self, value):
        if value == "on":
            if not self.state_is_on:
                self.state_is_on = True
        elif value == "off":
            if self.state_is_on:
                self.state_is_on = False
        else:
            raise ValueError("Invalid power state. Use 'on' or 'off'.")

    def set_channel(self, value):
        if not self.state_is_on:
            raise RuntimeError("The TV is off. Please turn it on first.")
        if value == "up":
            if self.state_current_channel < self.state_number_of_channels:
                self.state_previous_channel = self.state_current_channel
                self.state_current_channel += 1
            else:
                raise ValueError(f"Already at the highest channel "
                                 f"({self.state_number_of_channels}).")
        elif value == "down":
            if self.state_current_channel > 1:
                self.state_previous_channel = self.state_current_channel
                self.state_current_channel -= 1
            else:
                raise ValueError("Already at the lowest channel (1).")
        else:
            raise ValueError("Invalid channel command. Use 'up' or 'down'.")

    def get_state(self, detail="full"):
        if not self.state_is_on:
            return "The TV is off. Please turn it on first."
        if detail == "power":
            return "on" if self.state_is_on else "off"
        elif detail == "channel":
            return (f"{self.state_current_channel}/"
                    f"{self.state_number_of_channels}")
        elif detail == "channels":
            return str(self.state_number_of_channels)
        elif detail == "full":
            return (f"power: {'On' if self.state_is_on else 'Off'}\n"
                    f"channel: {self.state_current_channel}\n"
                    f"total channels: {self.state_number_of_channels}")
        else:
            raise ValueError("Unknown detail level. "
                             "Use 'full', 'power', 'channel', or 'channels'.")

