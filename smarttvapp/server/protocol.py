def parse_command(message):
    """Parse a client message and return a tuple: (command, attribute, value)
                                               or (command, None, None)
    """
    parts = message.strip().split()
    if not parts:
        return None, None, None
    command = parts[0]
    if command == "get":
        return "get", None, None
    elif command == "set" and len(parts) == 3:
        return "set", parts[1], parts[2]
    else:
        return None, None, None


def handle_protocol(tv, message):
    """Handle a client message using SmartTV and return a response string."""
    command, attribute, value = parse_command(message)
    if command == "get":
        # TODO: Implement the more granular get commands.
        return "Current state: " + "\n" + tv.get_state("full")
    elif command == "set":
        try:
            if attribute == "power":
                tv.set_power(value)
            elif attribute == "channel":
                tv.set_channel(value)
            else:
                return "Error: Unknown attribute. Use 'power' or 'channel'."
            return "state " + tv.get_state("full")
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Error: Unknown command. Please try again."
